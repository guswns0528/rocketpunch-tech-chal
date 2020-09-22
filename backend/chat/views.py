from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import ChatRoom


def login(request, username, password):
    user = authenticate(username=username, password=password):
    if user is not None:
        login(request, user)
        return JsonResponse({'msg': 'ok'})
    else:
        return JsonResponse({
            'msg': 'User dose not exist.',
            status=404)


def login_required(f):
    import functools

    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return f(request, *args, **kwargs)
        else:
            return JsonResponse({
                'msg': 'Login needed.'
                status=400})
    return wrapper


@login_required
def logout(request):
    logout(request)
    return JsonResponse({'msg': 'ok'})


@login_required
def create_chatroom(request, other_user):
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_add(~~~))
    pass


@login_required
def list_chatrooms(request):
    user = request.user
    rooms = Participant.objects.filter(user=user)
    return JsonResponse({'rooms': rooms})


@login_required
def get_last_messages(request, chatroom_id):
    user = request.user
    participant = get_object_or_404(
        Participant.objects.filter(user=user, room_id=chatroom_id)
    )
    messages = Message.objects.select_related('sender')
        .filter(room_id=chatroom_id)
        .order_by('created_at')[-50:0]
    return JsonResponse(
        [message.to_dict(prev_readed=participant.last_read_id)
            for message in messages]
    )


@login_required
def get_messages_since(request, chatroom_id, since):
    user = request.user
    participant = get_object_or_404(
        Participant.objects.filter(user=user, room_id=chatroom_id)
    )
    messages = Message.objects.select_related('sender')
        .filter(room_id=chatroom_id)
        .filter(pk__gt=since)
        .order_by('created_at')[-50:0]
    return JsonResponse(
        [message.to_dict(prev_readed=participant.last_read_id)
            for message in messages]
    )


@login_required
def send_message(request, chatroom_id, content):
    import datetime

    new_message = Message.objects.create(room_id=chatroom_id,
        user=request.user,
        content=content,
        created_at=datetime.now())
