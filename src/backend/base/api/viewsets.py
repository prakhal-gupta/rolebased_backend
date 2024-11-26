from rest_framework import mixins
from rest_framework.viewsets import ViewSetMixin as DRF_ViewSetMixin
from ..api import generics, views


class ViewSetMixin(DRF_ViewSetMixin):

    def check_action_permissions(self, request, action=None, obj=None):
        if action is None:
            action = self.action
        return super(ViewSetMixin, self).check_action_permissions(request, action=action, obj=obj)


class ViewSet(ViewSetMixin, views.APIView):
    pass


class GenericViewSet(ViewSetMixin, generics.GenericAPIView):

    def initial(self, request, *args, **kwargs):
        super(GenericViewSet, self).initial(request, *args, **kwargs)
        self.check_action_permissions(request)


class ModelViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, GenericViewSet):
    pass
