"""
URL configuration for dogonly_db project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dogonly_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.home, name = 'home'),
    path('help/', views.help, name = 'help'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('contact/send/', views.send_contact, name = 'send_contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_show, name='user_show'),
    path('users/edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>', views.user_delete, name='user_delete'),
    path('post/', views.post_create, name='post_create'),
    path('post/delete/<int:post_id>', views.post_delete, name='post_delete'),
    path('post-list', views.post_list, name='post_list')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
