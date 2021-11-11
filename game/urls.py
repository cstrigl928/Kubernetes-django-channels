
from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_board, name="game"),    # Core is defined from here we will use polls as alias for 'Core'...
]