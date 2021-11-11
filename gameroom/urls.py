
from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_room, name="game_room"),    # Core is defined from here we will use polls as alias for 'Core'...
]