import simplejson
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Participant, Message, ChatRoom, Connection
import asyncio


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
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
            return

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

        await self.accept()

    async def disconnect(self, code):
        user = self.scope['user']
        if user.is_anonymous:
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

    async def receive(self, data):
        # NOTE: Do I need to handle leaving a chat room?
        data = simplejson.loads(data)
        room_id = data['roomId']
        content = data['content']

        new_message = await store_message(user, room_id, content)

        await self.channel_layer.group_send(
            ChatRoom.room_id_to_room_name(room_id),
            {
                'type': 'handle_message',
                'message': new_message.to_dict(),
            }
        )

    async def handle_message(self, event):
        new_message = event['message']
        await self.send(simplejson.dumps({
            'type': 'MSG',
            **new_message
        }))

    async def join(self, event):
        join_msg = {
            'type': 'JOIN',
            'roomId': event['roomId'],
            'name': event['name']
        }
        await self.send(simplejson.dumps(join_msg))
