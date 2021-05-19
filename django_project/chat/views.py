from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatRoom, Participant, Message
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import Http404
import json
# Create your views here.
def index(request):
    chats = []
    for part in request.user.all_chats.all():
        users = part.chatroom.participants.all().exclude(id=request.user.id)
        if users:
            user = users[0]
            chats.append((part.chatroom.id, user))

    following = request.user.profile.following.all()[:5]
    context = {
        "chats": chats,
        "room": None, 
        "following": following
    }
    return render(request, 'chat/inbox.html', context)

def get_users(request):
    search_value = json.load(request)['search_value']
    query = Q(username__icontains=search_value) | Q(
        first_name__icontains=search_value)
    result = request.user.profile.following.all().filter(query)
    response = []
    for user in result:
        dictionary = {
            "username": user.username,
            "picture": user.profile.image.url,
            "name": f"{user.first_name} {user.last_name}",
            "chat_url": reverse('chat:get_chatroom', args=[user.id])
        }
        response.append(dictionary)
    print(response)
    return JsonResponse(response, safe=False)


def room(request, room_name):
    room = room_name
    context = {
        'room': room
    }

    return render(request, 'chat/room.html', context)


def get_chatroom(request, pk):
    # checks if the chatroom exists
    user = get_object_or_404(User, pk=pk)
    chat_exists = set()
    for part in request.user.all_chats.all().only('chatroom'):

        if user in part.chatroom.participants.all():
            # if exists, get that chat
            chatroom = part.chatroom
            chat_exists.add(True)
        else:
            chat_exists.add(False)

    if not True in chat_exists:
        #if  not, create the room
        chatroom = ChatRoom(created_by=request.user)
        chatroom.save()
        # then, add the participants to the chatroom
        participant1 = Participant(chatroom=chatroom, user=request.user)
        participant2 = Participant(chatroom=chatroom, user=user)
        participant1.save()
        participant2.save()
            
    # redirect to the chat view
    return redirect(reverse('chat:detail', args=[chatroom.id]))


def chatroom_detail(request, pk):
    chatroom = get_object_or_404(ChatRoom, pk=pk)
    # protecting the user for hardcoded url
    if not request.user in chatroom.participants.all():
        return redirect(reverse('chat:index'))

    messages = chatroom.all_messages.all()
    
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page', 1)
    if int(page_number) > paginator.num_pages:
        raise Http404("This page doesn't exists")
    page_obj = paginator.get_page(- int(page_number) + paginator.num_pages + 1)

    chats = []
    for part in request.user.all_chats.all():
        users = part.chatroom.participants.all().exclude(id=request.user.id)
        if users:
            user = users[0]
            chats.append((part.chatroom.id, user))

    context = {
        "chats": chats,
        "chat_messages": page_obj,
        "room": pk,
        "person": chatroom.participants.all().exclude(id=request.user.id)[0],
        "pages": paginator.num_pages
    }

    return render(request, "chat/detail.html", context)


def save_message(request, pk):
    text = json.load(request)['message']
    chatroom = get_object_or_404(ChatRoom, pk=pk)
    message = Message(chatroom=chatroom, sender=request.user, text=text)
    message.save()
    return HttpResponse("Success!")
