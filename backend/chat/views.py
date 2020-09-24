from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import ChatRoom, User, Participant, Message

import jwt

from backend.settings import SECRET_KEY


def check_method(method):
    def decorator(view):
        import functools

        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse(
                    {'msg': 'not available method'},
                    status=400)
            return view(request, *args, **kwargs)

        return wrapper
    return decorator


def check_post_parameter(name):
    def decorator(view):
        import functools

        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            if name not in request.POST:
                return JsonResponse(
                    {'msg': 'paramter constraint doesn\'t match'},
                    status=400)

            return view(request, *args, **kwargs)

        return wrapper
    return decorator


def login_required(f):
    import functools

    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        try:
            api_token = request.headers.get('Authorization', None)
            payload = jwt.decode(api_token, SECRET_KEY, algorithm='HS256')
            user = User.objects.get(pk=payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse(
                {
                    'msg': 'invalid token'
                },
                status=400
            )

        except User.DoesNotExist:
            return JsonResponse(
                {
                    'msg': 'invalid user'
                },
                status=400
            )

        return f(request, *args, **kwargs)
    return wrapper


@csrf_exempt
@check_method('POST')
@check_post_parameter('username')
@check_post_parameter('password')
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        # FIXME: set expiration date.
        # FIXME: jwt tokens cannot be revoked.

        token = jwt.encode({'user_id': user.pk}, SECRET_KEY, algorithm='HS256').decode('ascii')
        return JsonResponse({'apiToken': token})
    else:
        return JsonResponse(
            {'msg': 'User dose not exist.'},
            status=404)


@csrf_exempt
@login_required
def logout(request):
    # FIXME: revoke api token.
    return JsonResponse({'msg': 'ok'})


@csrf_exempt
@login_required
@check_method('POST')
@check_post_parameter('other_user_id')
def create_chatroom(request):
    from channels.layers import get_channel_layer

    # FIXME: this call can raises 404 error.
    # when 404 is raised, django renders html page.
    # In this backend project, all views are just json apis.
    # I have to return json with 404 when I can't find other user
    other_user = get_object_or_404(
        User.objects.get(pk=request.POST['other_user_id'])
    )

    try:
        with transaction.atomic():
            new_room = ChatRoom.create()
            new_room.save()

            participant = Participant(
                room=new_room,
                user=request.user,
                room_name=other_user.username
            )
            participant.save()
            other_participant = Participant(
                room=new_room,
                user=other_user,
                room_name=user.username
            )
            other_participant.save()

    except IntegrityError:
        return JsonResponse({'msg': 'failed to create a chatroom'}, status=400)

    channel_layer = get_channel_layer()
    # NOTE: maybe move to worker.
    participants_user_id = [participant, other_participant]
    for participant in participants:
        user_id = participant.user_id
        for connection in Connection.objects.filter(user_id=user_id):
            # TODO: check channel exist
            channel_name = connection.channel_name
            group_add = async_to_sync(channel_layer.group_add)
            group_add(
                ChatRoom.room_id_to_room_name(new_room.pk),
                channel_name
            )
    # NOTE: send ws message only the conversation partner.
    # Is this reasonable?
    # Or, just send a 200 resp and send join ws messages to user?
    for connection in Connection.objects.filter(user_id=other_participant.user_id):
        send = async_to_sync(channel_layer.send)
        send(channel_name, {
            'type': 'JOIN',
            'roomId': other_participant.room_id,
            'name': other_participant.room_name
        })

    return JsonResponse({'roomId': new_room.pk, 'name': participant.name})


@csrf_exempt
@login_required
@check_method('GET')
def list_chatrooms(request):
    user = request.user
    participants = Participant.objects.filter(user=user)
    rooms = [
        {
            'roomId': participant.room_id,
            'name': participant.room_name
        }
        for participant in participants
    ]
    return JsonResponse({'rooms': rooms})


@csrf_exempt
@login_required
def get_last_messages(request, chatroom_id):
    user = request.user
    # FIXME: return json object with 404 when failed to find object.
    participant = get_object_or_404(
        Participant.objects.filter(user=user, room_id=chatroom_id)
    )
    messages = (Message.objects.select_related('sender')
        .filter(room_id=chatroom_id)
        .order_by('created_at')[-50:0])

    # NOTE: Can I check a message readed with annotate method?
    messages = [message.to_dict() for message in messages]
    for message in messages:
        message['readed'] = message['msg_id'] <= participant.last_read_id
    return JsonResponse({'messages': messages})


@csrf_exempt
@login_required
def get_messages_before(request, chatroom_id, since):
    user = request.user
    # FIXME: return json object with 404 when failed to find object.
    participant = get_object_or_404(
        Participant.objects.filter(user=user, room_id=chatroom_id)
    )
    messages = (Message.objects.select_related('sender')
        .filter(room_id=chatroom_id)
        .filter(pk__gt=since)
        .order_by('created_at')[-50:0])

    # NOTE: Can I check a message readed with annotate method?
    messages = [message.to_dict() for message in messages]
    for message in messages:
        message['readed'] = message['msg_id'] <= participant.last_read_id

    return JsonResponse({'messages': messages})


@csrf_exempt
@login_required
@check_method('POST')
def message_read(request, chatroom_id, message_id):
    user = request.user
    participant = get_object_or_404(
        Participant.objects.filter(user=user, room_id=chatroom_id)
    )

    # FIXME: check a requested message is newer than stored in db.
    participant.last_read = Message.objects.get(pk=message_id)
    participant.save()

    return JsonResponse({'lastRead': participant.last_read_id})
