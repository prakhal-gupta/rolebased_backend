from .accounts.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import jwt
import threading

# Thread-local storage for request context
_thread_locals = threading.local()


class LogAllMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store request-specific information in thread-local storage
        _thread_locals.user_id = None
        _thread_locals.request_uri = request.META.get('PATH_INFO', None)

        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            token = token.split(" ")
            decoded = jwt.decode(token[-1], options={"verify_signature": False})
            _thread_locals.user_id = decoded.get("user_id", None)

        return self.get_response(request)

@receiver(pre_save)
def add_creator(sender, instance, **kwargs):
    user_id = getattr(_thread_locals, 'user_id', None)
    if not instance.pk and hasattr(instance, 'created_by') and user_id:
        try:
            instance.created_by = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            pass  # Handle the case where the user is not found
