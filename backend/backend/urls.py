from django.contrib import admin
from django.urls import path
from chat.views import (
    login, logout, list_chatrooms, create_chatroom, get_last_messages,
    get_messages_before, message_read
)

urlpatterns = [
    path('api/login/', login),
    path('api/logout/', logout),
    path('api/rooms/', list_chatrooms),
    path('api/chat/<int:chatroom_id>/', get_last_messages),
    path('api/chat_before/<int:chatroom_id>/<int:message_id>/', get_messages_before),
    path('api/new_chat/', create_chatroom),
    path('api/message_read/<int:chatroom_id>/<int:message_id>/', message_read),

    path('admin/', admin.site.urls),
]
