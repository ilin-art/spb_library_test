import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket-потребитель для обработки обмена сообщениями в чате."""
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        to_user_id = text_data_json['to_user_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'from_user_id': self.scope["user"].id,
        }), user_id=to_user_id)
