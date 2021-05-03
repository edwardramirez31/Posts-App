from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
        # obtener el chat de la url en scope
        self.chat_room = self.scope['url_route']['kwargs']['room_name']
        self.chat_group = f"chat_{self.chat_room}"

        # agregar el grupo con el nombre en string y el nombre del canal
        await self.channel_layer.group_add(self.chat_group, self.channel_name)
        # enviar mensajes al grupo
        # como segundo parametro se especifica que mensaje o evento se desea transmitir
        await self.channel_layer.group_send(self.chat_group, {
            "type": "tester.message",
            "tester": "hello_world"
        })

    # recibir cierto tipo de mensaje por parte de ese grupo

    async def tester_message(self, event):
        tester = event['tester']
        # enviar mensaje al servidor
        await self.send(text_data=json.dumps({
            "tester": tester
        }))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_group, self.channel_name)

    # receive message from the websocket
    async def receive(self, text_data):
        # obtener el objeto JSON como diccionario
        data = json.loads(text_data)
        # obtener el valor de la llave message
        message = data['message']
        username = data['user']
        # enviar al grupo
        await self.channel_layer.group_send(self.chat_group, {
            "type": "chat.message",
            "message": message,
            "username": username
        })

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

