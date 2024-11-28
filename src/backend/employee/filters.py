import django_filters
from django.db.models import Q
from ..customer.constants import GRIEVANCE_REJECTED, GRIEVANCE_APPROVED, GRIEVANCE_PENDING
from .models import GrievanceHODApproval, GrievanceHRApproval


class GrievanceHODApprovalFilter(django_filters.FilterSet):
    action_taken = django_filters.BooleanFilter(method='action_filter')
    start = django_filters.DateFilter(field_name='created_at__date', lookup_expr='gte')
    end = django_filters.DateFilter(field_name='created_at__date', lookup_expr='lte')

    class Meta:
        model = GrievanceHODApproval
        fields = {
            'id': ['exact'],
            'grievance': ['exact'],
            'action_by': ['exact'],
            'action_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'is_approved': ['exact'],
            'is_rejected': ['exact']
        }

    def action_filter(self, queryset, name, value):
        if value:
            return queryset.filter(Q(is_approved=value) | Q(is_rejected=value))
        else:
            return queryset.filter(is_approved=False, is_rejected=False)


class GrievanceHRApprovalFilter(django_filters.FilterSet):
    grievance_id = django_filters.NumberFilter(field_name='grievance__id', lookup_expr='exact')
    action_taken = django_filters.BooleanFilter(method='action_filter')
    start = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    status = django_filters.CharFilter(method='status_filter', lookup_expr='exact')

    class Meta:
        model = GrievanceHRApproval
        fields = {
            'id': ['exact'],
            'grievance': ['exact'],
            'approver': ['exact'],
            'action_by': ['exact'],
            'action_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'is_approved': ['exact'],
            'is_rejected': ['exact']
        }

    def action_filter(self, queryset, name, value):
        if value:
            return queryset.filter(Q(is_approved=value) | Q(is_rejected=value))
        else:
            return queryset.filter(is_approved=False, is_rejected=False)

    def status_filter(self, queryset, name, value):
        if value == GRIEVANCE_REJECTED:
            return queryset.filter(is_rejected=True)
        elif value == GRIEVANCE_APPROVED:
            return queryset.filter(is_approved=True)
        elif value == GRIEVANCE_PENDING:
            return queryset.filter(is_cancelled=False, is_rejected=False, is_approved=False)
        else:
            return queryset
