from django.shortcuts import render

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
            page_data["chess_form"] = chess_form


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
