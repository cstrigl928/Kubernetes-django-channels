from django.shortcuts import render

# -----
# To run locally, you need to open up 2-terminals:
# one to run our Cloud-Proxy, and another to run ./manage.py runserver:
#
# CMD1:
# --- 
# ./cloud_sql_proxy -instances="django-k8s-331621:us-west1:k8s-1"=tcp:5432
# CMD2:
# ---
# ./manage.py runserver
# Create your views here.
def chat(request):
    context = {'text':'Chat Page'}
    return render(request, 'chatwss/index.html', context)


def room(request, room_name):
    return render(request, 'chatwss/room.html', {
        'room_name': room_name,
    })