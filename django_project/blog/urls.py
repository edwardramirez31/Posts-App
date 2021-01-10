from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', HomeView, name='home'),
    path('about/', AboutView, name='about'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
]