import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_name = f"chat_{self.user.id}"
            self.room_group_name = f"chat_{self.user.id}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data["sender"]
        receiver_id = data["receiver"]
        message = data["message"]

        sender = await database_sync_to_async(User.objects.get)(id=sender_id)
        receiver = await database_sync_to_async(User.objects.get)(id=receiver_id)

        # Save message to MySQL
        await self.save_message(sender, receiver, message)

        # Send the message to the receiver
        await self.channel_layer.group_send(
            f"chat_{receiver_id}",
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
                "receiver": receiver.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
