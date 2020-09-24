from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import simplejson


User = get_user_model()


class ChatRoom(models.Model):

    def to_dict(self):
        return {'roomId': self.pk}

    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def room_id_to_room_name(cls, room_id):
        return f'chat_{room_id}'

    def __str__(self):
        return ChatRoom.room_id_to_room_name(self.pk)
    

class Participant(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_read = models.ForeignKey('Message', on_delete=models.DO_NOTHING, null=True, blank=True)
    room_name = models.CharField(max_length=150, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', 'room'])
        ]

        unique_together = [
            ['room', 'user']
        ]

    def to_dict(self):
        return {'roomId': self.room_id}


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['room', 'created_at'])
        ]

    @classmethod
    def create(cls, user, room, content):
        new_message = cls(
            sender=user,
            room=room,
            content=content,
            created_at=timezone.now()
        )
        return new_message

    def to_dict(self):
        return {
            'messageId': self.pk,
            'sender': self.sender.username,
            'content': self.content,
            'createdAt': self.created_at.isoformat(),
        }


class Connection(models.Model):
    # NOTE: where to store channel name? memory cache? rdbms?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # NOTE: https://channels.readthedocs.io/en/latest/channel_layer_spec.html#channel-semantics
    # Is 100 chars enough for channel name?
    channel_name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['user'])
        ]
