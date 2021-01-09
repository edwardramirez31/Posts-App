from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', HomeView, name='home'),
    path('about/', AboutView, name='about'),
]