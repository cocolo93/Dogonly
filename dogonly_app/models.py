from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        max_length=20
    )
    email = models.EmailField(
        unique=True
    )
    image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        default = 'images/default.png'
    )
    image_hash = models.CharField(
        max_length=64, unique=True, null=True
    )
    introduction = models.TextField(
        default='',
        blank=True,
        null=True,
        max_length=100,
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    content = models.TextField(
        max_length=100
    )
    image = models.ImageField(
        upload_to='contents/',
        blank=True,
        null=True,
    )
    image_hash = models.CharField(
        max_length=64, unique=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    ) 

    def __str__(self):  
        return f'{self.user.username}: {self.content[:20]}...' 

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    followed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} followed {self.followed_user.username}'

class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    liked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} liked  post {self.post.id}'