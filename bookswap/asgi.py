"""
ASGI config for bookswap project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.routine import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookswap.settings')

django_asgi_app = get_asgi_application()

# Verificar se o middleware foi inserido corretamente
application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AuthMiddlewareStack(
      URLRouter(
        websocket_urlpatterns  # Seu arquivo de roteamento para WebSockets
      )
  ),
})

print("ASGI application is being used.")
