from django.shortcuts import render

# Create your views here.

def chat(request):
    context = {}
    return render(request, 'chatwss/index.html', context)

def room(request, room_name):
    return render(request, 'chatwss/room.html', {
        'room_name': room_name
    })