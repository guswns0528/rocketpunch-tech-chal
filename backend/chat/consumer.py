import simplejson
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Participant, Message, ChatRoom, Connection
import asyncio


def get_participated(user):
    return Participant.objects.filter(user=user).all()


def store_message(user, room_id, content):
    # FIXME: handle invalid room_id
    room = ChatRoom.objects.get(pk=room_id)
    new_message = Message.create(user, room, content)
    new_message.save()
    return new_message


def create_connection(user, channel_name):
    client = Connection(user=user, channel_name=channel_name)
    client.save()
    return client

def delete_connection(connection_id):
    try:
        connection = Connection.objects.get(pk=connection_id)
        connection.delete()
    except:
        pass


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user = self.scope['user']

        participatedes = await database_sync_to_async(get_participated)()
        connection = await database_sync_to_async(create_connection)(
            user, channel_name
        )
        self.connection_id = connection.pk

        self.participated_rooms = [
            participated.room_id for participated in participatedes
        ]

        room_names = [
            ChatRoom.room_id_to_room_name(room)
            for room in self.participated_rooms
        ]
        await asyncio.wait([
            self.channel_layer.group_add(room_name, self.channel_name)
            for room_name in room_names
        ])

        await self.accept()

    async def disconnect(self):
        # NOTE: sometimes, disconnect fail to run.
        await database_sync_to_async(delete_connection)(self.connection_id)
        room_names = [
            ChatRoom.room_id_to_room_name(room)
            for room in self.participated_rooms
        ]
        await asyncio.wait([
            self.channel_layer.group_discard(room_name, self.channel_name)
            for room_name in room_names
        ])

    async def receive(self, data):
        # NOTE: Do I need to handle leaving a chat room?
        data = simplejson.loads(data)
        room_id = data['room_id']
        content = data['content']

        new_message = await database_sync_to_async(store_message)(
            user,
            room_id,
            content
        )

        await self.channel_layer.group_send(
            ChatRoom.room_id_to_room_name(room_id),
            {
                'type': 'handle_message',
                # FIXME
                'message': new_message.to_dict(new_message.pk - 1),
            }
        )

    async def handle_message(self, event):
        new_message = event['message']
        await self.send(new_message)
