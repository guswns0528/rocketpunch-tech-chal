from channels.routing import URLRouter
from django.urls import path

from . import consumer

patterns = URLRouter([
    path(r'ws/chat/', consumer.ChatConsumer),
])
