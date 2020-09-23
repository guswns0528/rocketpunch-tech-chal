from channels.routing import URLRouter
from django.urls import path

from . import consumer
from .util import TokenAuthMiddlewareStack

patterns = TokenAuthMiddlewareStack(
    URLRouter([
        path(r'ws/chat/', consumer.ChatConsumer),
    ])
)
