from django.contrib import admin
from .models import ChatRoom, Participant, Message


class ChatRoomAdmin(admin.ModelAdmin):
    fields = []


class ParticipantAdmin(admin.ModelAdmin):
    fields = ['room', 'user', 'room_name', 'last_read']


class MessageAdmin(admin.ModelAdmin):
    fields = ['room', 'sender', 'content', 'created_at']


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message, MessageAdmin)
