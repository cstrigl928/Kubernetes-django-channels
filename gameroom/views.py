from django.shortcuts import render

# Create your views here.
def mainGameRoom(request):
    return render(request, 'gameroom/main.html', {
        'context': request.user,
    })

def game_room(request, room_name):
    context = {}
    return render(request, 'gameroom/room_copy.html', {
        'req-users':request.user,
        'room_name': room_name,
    })