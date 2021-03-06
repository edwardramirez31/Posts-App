"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    # Si quiero que el blog sea la pagina home del website solo
    # quito el path y dejo vacio tanto acá como en blog.urls
    # path('blog/', include('blog.urls')),
    path('', include('blog.urls')),
    path('chat/', include('chat.urls')),
    path('notifications/', include('notifications.urls')),
    path('register/', users_views.Register.as_view(), name = 'register'),
    path('profile/<int:pk>', users_views.profile , name = 'profile'),
    path('profiles/', users_views.profiles , name = 'profiles'),
    path('update_profile/', users_views.update_profile , name = 'update_profile'),
    path('follow/<int:pk>', users_views.follow , name = 'follow'),
    path('unfollow/<int:pk>', users_views.unFollow , name = 'un_follow'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'), name = 'password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name = 'password_reset_complete'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
