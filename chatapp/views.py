from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import uuid
from django.db.models import Count
from portal.models import User
from .models import Room, Message, PersonalMessage
from .forms import CreateRoomForm
# Create your views here.


def list_rooms(request):
    rooms = Room.objects.all()
    return render(request, "chatapp/chatrooms.html",{"rooms":rooms, "user":request.user})

@login_required
def list_room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, "chatapp/room.html", {"room": room, "messages":messages})

@login_required
def delete_room(request, slug):
    room = Room.objects.get(slug=slug)
    room.delete()
    return redirect("list-rooms")

@login_required
def get_personal_messages(request, username=None):
    receiver = User.objects.get(username=username)
    messages = PersonalMessage.objects.filter(sender=request.user, receiver=receiver) | PersonalMessage.objects.filter(sender=receiver, receiver=request.user)
    print(messages)
    return render(request, "chatapp/chat.html", {"messages":messages, "receiver":receiver})

@login_required
def get_users_message_list(request):
    user = request.user
    list_of_users = PersonalMessage.objects.filter(receiver=user)| PersonalMessage.objects.filter(sender=user)
    set_of_users = set()
    for i in list_of_users:
        if i.sender == user:
            set_of_users.add(i.receiver)
        else:
            set_of_users.add(i.sender)
    print(set_of_users)
    return render(request, "chatapp/users_message_list.html", {"list_of_users":set_of_users})

@login_required
def create_room(request):
    form = CreateRoomForm()
    if request.method == "POST":
        form = CreateRoomForm(request.POST)
        slugfield = uuid.uuid4()
        if form.is_valid():
            form.save(slugfield, request.user)
            return redirect(f'/room/{slugfield}/')
    return render(request, "chatapp/createroom.html")