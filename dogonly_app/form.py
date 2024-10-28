from django import forms
from .models import User, Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['checkbox_name'] = name + '_clear'
        context['checkbox_id'] = attrs.get('id') + '_clear'
        context['checkbox_label'] = 'Clear'
        return context

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('image', 'username', 'name', 'email')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Password Confirmation" 
        for fieldname in ['username', 'password1', 'password2', 'email']:
            self.fields[fieldname].help_text = None 

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', 'name', 'email', 'introduction')
        widgets = {
            'image': CustomClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['introduction'].label = "Introduction"
        for fieldname in ['name', 'email', 'introduction']:
            self.fields[fieldname].help_text = None 
    
    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        if not self.cleaned_data.get('image'):
            user.image = 'profile/images/default.png'
        if commit:
            user.save()
        return user

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image')

class LoginForm(AuthenticationForm):
    pass
