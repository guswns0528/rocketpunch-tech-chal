from django.urls import path

from . import consumer

patterns = [
    path(r'ws/chat/<int:room_id>', consumer.ChatConsumer),
]
