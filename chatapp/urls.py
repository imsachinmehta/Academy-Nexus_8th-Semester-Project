from django.urls import path

from . import views

urlpatterns = [
    path("chatrooms/", views.list_rooms, name="list-rooms"),
    path("room/<slug:slug>/", views.list_room, name="room"),
    path("chatrooms/createroom/", views.create_room, name="create-room"),
    path("chatrooms/delete/<slug:slug>/", views.delete_room, name="delete-room"),
    # path("chat/<str:username>/", views.one_to_one_chat, name="chat-personally"),
    path("personal_messages/", views.get_users_message_list, name="users-list"),
    path(
        "personal_messages/<str:username>/",
        views.get_personal_messages,
        name="personal-messages",
    ),
]
