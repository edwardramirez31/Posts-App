from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.urls import reverse

class UserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.user_id = self.scope['url_route']['kwargs']['user']
        self.user_group = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.user_group, self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def new_follow(self, event):
        message = event['message']
        picture = event['picture']
        url = event['url']
        await self.send(text_data=json.dumps({
            "message": message,
            "picture": picture,
            "url": url
        }))
