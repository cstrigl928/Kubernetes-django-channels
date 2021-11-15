# Async gateway Server Protocal (ASGI) used for websockets/ Asynchronous
# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chatwss.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            URLRouter(
                chatwss.routing.websocket_urlpatterns
            )
    ),
})

print("routing correctly\n\n")