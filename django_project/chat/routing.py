from django.urls import re_path
from .consumers import ChatRoomConsumer

ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$',
            ChatRoomConsumer.as_asgi(), name='char_consumer'),
]
