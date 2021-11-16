# Use this the same we use URLs.py, accept for WS-connections.

from django.urls.conf import path
from . import consumers
from django.urls import re_path

websocket_urlpatterns = [ 
    path('ws/game-room/', consumers.GameRoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.GameRoomConsumer.as_asgi()),
]