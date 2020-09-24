from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Participant, Message, ChatRoom, Connection, User

from backend.settings import SECRET_KEY

import simplejson
import asyncio
import jwt


@database_sync_to_async
def get_user(api_token):
    try:
        payload = jwt.decode(api_token, SECRET_KEY, algorithm='HS256')
        user = User.objects.get(pk=payload['user_id'])
    except jwt.exceptions.DecodeError:
        return None
    except User.DoesNotExist:
        return None
    return user


@database_sync_to_async
def get_participated(user):
    records = Participant.objects.filter(user=user).all()
    return [participated.room_id for participated in records]


@database_sync_to_async
def store_message(user, room_id, content):
    # FIXME: handle invalid room_id
    room = ChatRoom.objects.get(pk=room_id)
    new_message = Message.create(user, room, content)
    new_message.save()
    return new_message


@database_sync_to_async
def create_connection(user, channel_name):
    client = Connection(user=user, channel_name=channel_name)
    client.save()
    return client


@database_sync_to_async
def delete_connection(connection_id):
    try:
        connection = Connection.objects.get(pk=connection_id)
        connection.delete()
    except:
        pass


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # just accept
        self.user = None
        await self.accept()

    async def disconnect(self, code):
        user = self.user
        if user is None:
            return

        # NOTE: sometimes, disconnect fail to run.
        await delete_connection(self.connection_id)
        room_names = [
            ChatRoom.room_id_to_room_name(room)
            for room in self.participated_rooms
        ]
        await asyncio.wait([
            self.channel_layer.group_discard(room_name, self.channel_name)
            for room_name in room_names
        ])

    async def receive(self, text_data=None, bytes_data=None):
        # NOTE: Do I need to handle leaving a chat room?
        data = simplejson.loads(text_data)
        message_type = data.get('type', None)
        if message_type == 'auth':
            user = await get_user(data['apiToken'])
            if user is None:
                await self.close()
                return

            self.user = user
            connection = await create_connection(user, self.channel_name)
            self.participated_rooms = await get_participated(user)
            self.connection_id = connection.pk

            room_names = [
                ChatRoom.room_id_to_room_name(room)
                for room in self.participated_rooms
            ]
            await asyncio.wait([
                self.channel_layer.group_add(room_name, self.channel_name)
                for room_name in room_names
            ])
            return
        elif self.user is None:
            await self.close()

        user = self.user
        room_id = data.get('roomId', None)
        if room_id is None:
            return
        # TODO: sanitize content.
        content = data.get('content', None)
        if content is None:
            return

        new_message = await store_message(user, room_id, content)

        await self.channel_layer.group_send(
            ChatRoom.room_id_to_room_name(room_id),
            {
                'type': 'handle_message',
                'message': new_message.to_dict(),
                'roomId': new_message.room_id
            }
        )

    async def handle_message(self, event):
        if self.user is None:
            return
        new_message = event['message']
        await self.send(simplejson.dumps({
            'type': 'MSG',
            'roomId': event['roomId'],
            'message': {**new_message}
        }))

    async def join(self, event):
        if self.user is None:
            return
        join_msg = {
            'type': 'JOIN',
            'roomId': event['roomId'],
            'name': event['name']
        }
        await self.send(simplejson.dumps(join_msg))
