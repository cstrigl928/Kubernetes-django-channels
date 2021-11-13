# chat/routing.py
from django.urls import re_path

from . import consumers
print("BEFORE CONSUMES!")
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
print("\n\nConsumers!!")