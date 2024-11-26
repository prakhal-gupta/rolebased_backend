from rest_framework import generics as DRF_generics
from rest_framework import exceptions


class GenericAPIView(DRF_generics.GenericAPIView):
    def get_object(self):
        obj = super(GenericAPIView, self).get_object()
        self.check_action_permissions(self.request, self.action, obj)
        return obj

    def check_action_permissions(self, request, action, obj=None):
        if action is None:
            self.permission_denied(request)

        for permission in self.get_permissions():
            if not permission.has_action_permission(request, self, action, obj):
                self.permission_denied(request)


class LawsphereGenericAPIView(GenericAPIView):
    def app_permission_denied(self, request, message=None):
        if not request.successful_authenticator and not message:
            raise exceptions.NotAuthenticated()
        if message:
            raise exceptions.PermissionDenied(detail=message)
        raise exceptions.PermissionDenied(detail=message)
