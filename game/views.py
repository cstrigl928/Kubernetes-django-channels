from django.shortcuts import render

# Create your views here.
def game_board(request):
    context = {}
    return render(request, 'game/board.html', context)