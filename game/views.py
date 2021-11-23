from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from game.models import Board
from game.forms import ChessForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def newGame(request):
    page_data = {
    "rows": [
    {"a8": "&#9820;", "b8": "&#9822;", "c8":"&#9821;", "d8": "&#9819;", "e8": "&#9818;", "f8": "&#9821;", "g8": "&#9822;", "h8": "&#9820;"},
    {"a7": "&#9823;", "b7":"&#9823;", "c7": "&#9823;", "d7": "&#9823;", "e7": "&#9823;", "f7": "&#9823;", "g7": "&#9823;", "h7": "&#9823;"},
    {"a6": "&nbsp;", "b6": "&nbsp;", "c6": "&nbsp;", "d6": "&nbsp;", "e6": "&nbsp;", "f6": "&nbsp;", "g6": "&nbsp;", "h6": "&nbsp;"},
    {"a5": "&nbsp;", "b5": "&nbsp;", "c5": "&nbsp;", "d5": "&nbsp;", "e5": "&nbsp;", "f5": "&nbsp;", "g5": "&nbsp;", "h5": "&nbsp;"},
    {"a4": "&nbsp;", "b4": "&nbsp;", "c4": "&nbsp;", "d4": "&nbsp;", "e4": "&nbsp;", "f4": "&nbsp;", "g4": "&nbsp;", "h4": "&nbsp;"},
    {"a3": "&nbsp;", "b3": "&nbsp;", "c3": "&nbsp;", "d3": "&nbsp;", "e3": "&nbsp;", "f3": "&nbsp;", "g3": "&nbsp;", "h3": "&nbsp;"},
    {"a2": "&#9817;", "b2": "&#9817;", "c2": "&#9817;", "d2": "&#9817;", "e2": "&#9817;", "f2": "&#9817;", "g2": "&#9817;", "h2": "&#9817;"},
    {"a1": "&#9814;", "b1": "&#9816;", "c1": "&#9815;", "d1": "&#9813;", "e1": "&#9812;", "f1": "&#9815;", "g1": "&#9816;", "h1": "&#9814;"}
    ]
    }

    Board.objects.filter(user=request.user).delete()


    for row in page_data.get("rows"):
        for id, val in row.items():
            Board(user=request.user, location=id, value=val).save()

@login_required(login_url='/login/')
def game_board(request):

    if ((Board.objects.filter(user=request.user).count() == 0) or (request.method == 'GET' and 'new_game' in request.GET)):
        newGame(request)

    page_data = { "rows": [], "chess_form": ChessForm }

    if (request.method == 'POST'):
        chess_form = ChessForm(request.POST)
        if (chess_form.is_valid()):
            location = chess_form.cleaned_data["location"]
            fromLoc = location[:2]
            toLoc = location[2:]
            value = ""
            try:
                value = Board.objects.get(user=request.user, location=fromLoc).value
            except Board.DoesNotExist:
                value = "&nbsp;"

            Board.objects.filter(user=request.user, location=toLoc).delete();
            Board.objects.filter(user=request.user, location=fromLoc).delete();
            Board(user=request.user, location=toLoc, value=value).save()
            Board(user=request.user, location=fromLoc, value="&nbsp;").save()
        else:
            page_data["chess_fo rm"] = chess_form


    for row in range (8,0,-1):
        row_data = {}
        for col in ['a','b','c','d','e','f','g','h']:
            id = str(col)+str(row)
            try:
                record = Board.objects.get(user=request.user, location=id)
                row_data[id] = record.value
            except Board.DoesNotExist:
                row_data[id] = "&nbsp;"
        page_data.get("rows").append(row_data)

    return render(request, 'game/board.html', page_data)
