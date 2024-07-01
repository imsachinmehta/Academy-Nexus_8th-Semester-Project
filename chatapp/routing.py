from django.urls import path
from .consumer import ChatConsumer, PersonalChatConsumer

websocket_urlpatterns = [
    path("ws/chatroom/<str:room_slug>/", ChatConsumer.as_asgi()),
    path("ws/chat/<str:username>/", PersonalChatConsumer.as_asgi()),
]