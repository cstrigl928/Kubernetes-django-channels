
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainGameRoom, name='main-room'),
    path('<str:room_name>/', views.game_room, name="game_room"),    # Core is defined from here we will use polls as alias for 'Core'...
]