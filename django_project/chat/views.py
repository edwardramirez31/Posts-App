from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    room = room_name
    context = {
        'room': room
    }

    return render(request, 'chat/room.html', context)