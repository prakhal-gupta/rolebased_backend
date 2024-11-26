import django_filters
from django.db.models import Q

from .models import User


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
            'is_separated': ['exact']
        }
