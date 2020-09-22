from django.db import models
from django.contrib.auth import get_user_model
import simplejson


User = get_user_model()


class ChatRoom(models.Model):

    def to_dict(self):
        return {'room_id': self.pk}
    

class Participant(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_read = models.ForeignKey('Message', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', 'room'])
        ]

        unique_together = [
            ['room', 'user']
        ]

    def to_dict(self):
        return {'room_id': self.room_id}


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['room', 'created_at'])
        ]

    def to_dict(self, prev_readed=None):
        return {
            'msg_id': self.pk,
            'sender': self.sender.username,
            'content': self.content,
            'created_at': self.created_at,
            'readed': prev_readed and self.pk <= prev_readed or False
        }

