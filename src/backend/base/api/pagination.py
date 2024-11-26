import json
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        extra = None
        if not hasattr(self, 'page'):
            return Response(data)
        if type(data) == type(dict()):
            extra = data.get("extra", None)
            data = data.get('data', [])
        next_page = self.page.number + 1 if self.get_next_link() else None
        prev_page = self.page.number - 1 if self.get_previous_link() else None
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('next', next_page),
            ('previous', prev_page),
            ('extra', extra),
            ('results', data)
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        if not json.loads(request.query_params.get("pagination", "true")):
            return queryset
        return super().paginate_queryset(queryset, request, view)


class StandardResultsSetPagination(DefaultPageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50
