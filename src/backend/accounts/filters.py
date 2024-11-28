import django_filters
from .models import User, Roles


class UserBasicFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'first_name': ['icontains'],
            'middle_name': ['icontains'],
            'last_name': ['icontains'],
            'mobile': ['icontains'],
            'email': ['icontains'],
            'is_separated': ['exact'],
            'role': ['exact'],
        }

class RolesFilter(django_filters.FilterSet):
    ids = django_filters.CharFilter(method='ids_filter')

    class Meta:
        model = Roles
        fields = {
            'id': ['exact'],
            'code_name': ['icontains'],
            'name': ['icontains']
        }

    def ids_filter(self, queryset, name, value):
        return queryset.filter(id__in=value.split(","))

