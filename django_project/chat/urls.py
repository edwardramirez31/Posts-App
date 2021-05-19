from django.urls import path
from .views import index, room, get_chatroom, chatroom_detail, save_message, get_users

app_name = "chat"

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('getroom/<int:pk>/', get_chatroom, name='get_chatroom'),
    path('detail/<int:pk>/', chatroom_detail, name='detail'),
    path('save/<int:pk>/', save_message, name='save_message'),
    path('get_users/all/', get_users, name='get_users'),
]