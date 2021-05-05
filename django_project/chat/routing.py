from django.urls import re_path
from .consumers import ChatRoomConsumer, ChatConsumer
from notifications.consumers import UserConsumer

ws_urlpatterns = [
    re_path(r'ws/(?P<user>\w+)/$',
            UserConsumer.as_asgi(), name='user_socket'),
    re_path(r'ws/chat/(?P<room_name>\w+)/$',
            ChatRoomConsumer.as_asgi(), name='char_consumer'),
    re_path(r'ws/chatroom/(?P<room_name>\w+)/$',
            ChatConsumer.as_asgi(), name='chat_consumer'),
]
