# Async gateway Server Protocal (ASGI) used for websockets/ Asynchronous
# mysite/asgi.py
import os

from channels.auth import AuthMiddleware, AuthMiddlewareStack    # Added To Route ASGI to our Consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

import chatwss.routing as chat_routing
print(f"Routing: { chat_routing }")

# from chatwss.routing import AuthMiddlewareStack, URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# ProtocolTypeRouter: Inspects the type of connection made (either Http/Https or WS/WSS)
    # Examins the HTTP path of the connection to route it to a Particular Consumer,
    #  routing is based on the Provided URL patterns.
    # e.g. If 'Request' starts (prefixed) with 'WS' or 'WSS' then routes to websocket-routing consumers
application = ProtocolTypeRouter({
<<<<<<< HEAD
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            URLRouter(
                chatwss.routing.websocket_urlpatterns
            )
    ),
})

print("routing correctly\n\n")
=======
    # Just HTTP for now. (We can add other protocols later.)
    "http": get_asgi_application(),
    # Add Websocket Connection
    # AuthMiddleWareStack: Populate the connection 'SCOPE' with a reference to currently Authenticated User. Also
    # Allows us to still utilize the 'request.<method_name>' within our templates after request is sent back to User.
    # URLRouter: Examines the HTTP path of the connection & Routes it to the particular Consumer instance, based on its provided URL patterns
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns
        )
    ),

})
>>>>>>> origin/remote-staging
