# Async gateway Server Protocal (ASGI) used for websockets/ Asynchronous
# mysite/asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddleware, AuthMiddlewareStack    # Added To Route ASGI to our Consumers
from channels.routing import ProtocolTypeRouter

import chatwss.routing
print(f"Routing: { chatwss.routing }")

# from chatwss.routing import AuthMiddlewareStack, URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    # Just HTTP for now. (We can add other protocols later.)
    "http": get_asgi_application(),
    # Add Websocket Connection
    # Examins the HTTP path of the connection to route it to a Particular Consumer,
    #  routing is based on the Provided URL patterns.
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatwss.routing.websocket_urlpatterns
        )
    ),

})