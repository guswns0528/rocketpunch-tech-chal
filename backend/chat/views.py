from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .models import ChatRoom, User, Participant, Message


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
        if request.user.is_authenticated:
            return f(request, *args, **kwargs)
        else:
            return JsonResponse({
                'msg': 'Login needed.'},
                status=400)
    return wrapper


@check_method('POST')
@check_post_parameter('username')
@check_post_parameter('password')
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'msg': 'ok'})
    else:
        return JsonResponse(
            {'msg': 'User dose not exist.'},
            status=404)


@login_required
def logout(request):
    logout(request)
    return JsonResponse({'msg': 'ok'})


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
        User.object.get(pk=request.POST['other_user_id'])
    )

    try:
        with transaction.atomic():
            new_room = ChatRoom.create()
            new_room.save()

            participant = Participant(room=new_room, user=request.user)
            participant.save()
            other_participant = Participant(room=new_room, user=other_user)
            other_participant.save()

    except IntegrityError:
        return JsonResponse({'msg': 'failed to create a chatroom'}, status=400)

    channel_layer = get_channel_layer()
    participants_user_id = [participant.user_id, other_participant.user_id]
    for user_id in participants_user_id:
        for connection in Connection.objects.filter(user_id=user_id):
            # TODO: check channel exist
            channel_name = connection.channel_name
            group_add = async_to_sync(channel_layer.group_add)
            group_add(
                ChatRoom.room_id_to_room_name(new_room.pk),
                channel_name
            )

    return JsonResponse({})


@login_required
@check_method('GET')
def list_chatrooms(request):
    user = request.user
    rooms = Participant.objects.filter(user=user)
    return JsonResponse({'rooms': rooms})


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
