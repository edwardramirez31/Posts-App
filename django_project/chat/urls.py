from django.urls import path
from .views import index, room

app_name = "chat"

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', room, name='room'),
]