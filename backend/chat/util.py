from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from backend.settings import SECRET_KEY
from .models import User

import jwt


@database_sync_to_async
def get_user(headers):
    try:
        token_type, api_token = headers[b'Authorization'].split()
        if token_type != 'Bearer':
            return AnonymousUser()
        payload = jwt.decode(api_token, SECRET_KEY, algorithm='HS256')
        user = User.objects.get(pk=payload['user_id'])
        return user
    except jwt.exceptions.DecodeError:
        return AnonymousUser()
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            self.scope['user'] = await get_user(headers)
        inner = self.inner(self.scope)
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
