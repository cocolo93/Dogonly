
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .form import SignupForm, LoginForm, EditForm, PostCreateForm
from django.contrib.auth import login, logout, get_user_model
from .models import Post, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .predict import predict
import hashlib, time, os, environ
from django.contrib import messages
from django.conf import settings

def generate_image_hash(image_file):
    hash_md5 = hashlib.sha256()

    current_time = str(time.time()).encode('utf-8')
    hash_md5.update(current_time)

    for chunk in iter(lambda: image_file.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/home.html', {'posts': posts})

def help(request):
    return render(request, 'pages/help.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def send_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        category = request.POST.get('category')
        inquiry = request.POST.get('inquiry')

        subject = f'from: {name} - category: {category}'
        message = f'From: {email}\n\nInquiry: {inquiry}'
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(
            subject,
            message,
            email,
            recipient_list,
        )
        return render(request, 'pages/thanks.html')


def signup(request):
    if request.method == 'POST':

        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            if 'image' not in request.FILES:
                user.image = 'images/default.png' 
            else:
                image_hash = generate_image_hash(request.FILES['image'])
                user.image_hash = image_hash
                image_filename = f"{user.image_hash}.png"
                user.image.name = image_filename 
            user.save()
            login(request, user)
            return redirect('mypage')
    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'users/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                if next == 'None':
                    return redirect(to='/mypage/')
                else:
                    return redirect(to=next)
    else:
        form = LoginForm()
        next = request.GET.get('next')

    param = {
        'form': form,
        'next': next
    }

    return render(request, 'users/login.html', param)

@login_required
def logout_view(request):
    logout(request)

    return render(request, 'users/logout.html')

@login_required
def mypage(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')

    params = {
        'user': user,
        'posts': posts
    }

    return render(request, 'users/mypage.html', params)

@login_required
def user_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('date_joined')
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/user_list.html', {'users': users, 'page_obj': page_obj})

@login_required
def user_show(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    params = {
        'user': user,
        'posts': posts
    }
    return render(request, 'users/user_show.html', params)

@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user != user:
        return redirect('user_list') 

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'image' in request.FILES:
                user.image = request.FILES['image']
                image_hash = generate_image_hash(request.FILES['image'])
                user.image_hash = image_hash
                image_filename = f"{user.image_hash}.png"
                user.image.name = image_filename 
            elif 'image-clear' in request.POST:
                user.image = 'images/default.png'
            user.name = form.cleaned_data.get('name', user.name)
            user.email = form.cleaned_data.get('email', user.email)
            user.introduction = form.cleaned_data.get('introduction', user.introduction)
            user.save()
            return redirect('mypage')
    else:
        form = EditForm(instance=user)

    return render(request, 'users/edit.html', {'form': form})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
            user.delete()
            return redirect('home')
    return redirect('home')

@login_required
def post_create(request):
    user = request.user

    if request.method == 'POST':

        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.image = request.FILES['image']
            category = predict(post.image)
            if category != 'dog':
                messages.error(request, 'This social networking site only allows you to post pictures of a dog.')
                return redirect('post_create')
            image_file = request.FILES['image']
            image_hash = generate_image_hash(image_file)
            post.image_hash = image_hash
            image_filename = f"{post.image_hash}.png"
            post.image.name = image_filename 
            post.save()
            return redirect('mypage')
    else:
        form = PostCreateForm()
    
    param = {
        'form': form
    }

    return render(request, 'posts/create.html', param)

@login_required
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/post_list.html', {'posts': posts, 'page_obj': page_obj})

@login_required
def post_delete(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        if post.user == user:
            post.delete()
            return redirect('mypage')
    return redirect('mypage')
