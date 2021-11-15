# chat/routing.py
from django.urls import re_path

from . import consumers
<<<<<<< HEAD
print("route mother fucker\n\n")
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
print("again mfer\n")
=======
print("Routing Consumers")
# once the WS-request is seen - WS-URL_patterns sends the ws-Request to its associated Consumer in consumers.py
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

print("\n\nFinished Routing ..")
>>>>>>> origin/remote-staging
