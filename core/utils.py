import json

import jwt

from django.http  import JsonResponse
from users.models import User
from django.conf  import settings

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            user_id      = payload['user_id']
            request.user = User.objects.get(id = user_id)

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({ 'message' : 'INVALID_TOKEN' }, status = 400)
        
        except KeyError:
            return JsonResponse({ 'message' : 'KEY_ERROR' }, status = 400)

    return wrapper