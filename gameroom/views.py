from django.shortcuts import render

# Create your views here.
def game_room(request):
    context = {}
    return render(request, 'gameroom/room.html', context)