from django.contrib import admin
from .models import ChatRoom, Participant, Message


class ChatRoomAdmin(admin.ModelAdmin):
    pass


class ParticipantAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message, MessageAdmin)
