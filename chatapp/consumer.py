import json
from channels.exceptions import StopConsumer

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from portal.models import User
from .models import Room, Message, PersonalMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f"chat_{self.room_slug}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        raise StopConsumer()

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room_slug = data['room_slug']

        await self.save_message(message, username, room_slug)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room_slug': room_slug,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room_slug = event['room_slug']

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "room_slug": room_slug,
        }))

    @sync_to_async
    def save_message(self, message, username, room_slug):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_slug)
        Message.objects.create(user=user, room=room, content=message)

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        receiver_username = self.scope['url_route']['kwargs']['username']
        reciever = await self.get_user(receiver_username)
        sender = self.scope['user']

        if sender.id > reciever.id:
            self.room_group_name = f"personal_chat_{reciever.id}_{sender.id}"
        else:
            self.room_group_name = f"personal_chat_{sender.id}_{reciever.id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"Disconnect with exit code {close_code}")
        raise StopConsumer()

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        receiver = await self.get_user(data['username'])
        sender = self.scope['user']
        if message:
            await self.save_message(sender, receiver, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": receiver.username,
            }
        )
    async def chat_message(self, event):
        message = event['message']
        receiver_username = event['username']
        await self.send(text_data=json.dumps({
            "message": message,
            "username": receiver_username,
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message):
        PersonalMessage.objects.create(sender=sender, receiver=receiver, content=message)