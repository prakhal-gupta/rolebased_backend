import django_filters
from django.db.models import Q
from .models import DynamicSettings, Country, State, City, Employee

class DynamicSettingsFilter(django_filters.FilterSet):
    parents = django_filters.CharFilter(method='parents_filter', lookup_expr='exact')

    class Meta:
        model = DynamicSettings
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'value': ['exact', 'icontains'],
            'parent': ['exact']
        }

    def parents_filter(self, queryset, name, value):
        return queryset.filter(parent__in=value.split(","))


class CountryFilter(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
        }


class StateFilter(django_filters.FilterSet):
    class Meta:
        model = State
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'country': ['exact'],
        }


class CityFilter(django_filters.FilterSet):
    class Meta:
        model = City
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'state': ['exact'],
        }


class EmployeeFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='custom_filter')
    date = django_filters.DateFilter(method='datewise_report_filter')
    month = django_filters.DateFilter(method='monthly_report_filter')
    start_date = django_filters.CharFilter(field_name='created_at__date', lookup_expr='gte')
    end_date = django_filters.CharFilter(field_name='created_at__date', lookup_expr='lte')
    month_from = django_filters.DateFilter(method='month_from_report_filter')
    month_to = django_filters.DateFilter(method='month_to_report_filter')

    class Meta:
        model = Employee
        fields = {
            'id': ['exact'],
            'user': ['exact'],
            'permission_set': ['exact'],
            'designation': ['exact'],
            'department': ['exact'],
            'joining_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'status': ['exact'],
            'is_primary': ['exact'],
            'is_disabled': ['exact'],
            'is_active': ['exact']
        }

    def custom_filter(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(mobile__icontains=value) |
                               Q(designation__icontains=value) | Q(user__first_name__icontains=value) |
                               Q(user__mobile__icontains=value) | Q(user__email__icontains=value))

    def datewise_report_filter(self, queryset, name, value):
        return queryset.filter(Q(created_at__date=value))

    def monthly_report_filter(self, queryset, name, value):
        return queryset.filter(Q(created_at__month=value.month) & Q(created_at__year=value.year))

    def month_from_report_filter(self, queryset, name, value):
        return queryset.filter(created_at__month__gte=value.month, created_at__year__gte=value.year)

    def month_to_report_filter(self, queryset, name, value):
        return queryset.filter(created_at__month__lte=value.month, created_at__year__lte=value.year)
