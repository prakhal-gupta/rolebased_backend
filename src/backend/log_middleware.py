from .accounts.models import User
from django.db.models.signals import *
from django.dispatch import receiver
import jwt


class LogAllMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global user_id
        global request_uri
        user_id = None
        request_uri = request.META.get('PATH_INFO', None)
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            token = token.split(" ")
            decoded = jwt.decode(token[-1], options={"verify_signature": False})
            user_id = decoded.get("user_id", None)
        return self.get_response(request)

    @receiver(pre_save)
    def add_creator(sender, instance, **kwargs):
        if not instance.pk and hasattr(instance, 'created_by') and user_id:
            instance.created_by = User.objects.get(id=user_id, is_active=True)
        return instance


