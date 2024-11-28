import django_filters

from .constants import GRIEVANCE_REJECTED, GRIEVANCE_APPROVED, GRIEVANCE_PENDING
from .models import Customer, Grievance

class CustomerFilter(django_filters.FilterSet):

    class Meta:
        model = Customer
        fields = {
            'user': ['exact'],
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'mobile': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'aadhar_no': ['exact', 'icontains'],
            'pan_no': ['exact', 'icontains'],
            'father_name': ['exact', 'icontains'],
            'state': ['exact'],
            'city': ['exact'],
            'address': ['exact', 'icontains'],
            'pincode': ['exact', 'icontains'],
            'is_active': ['exact'],
        }


class GrievanceFilter(django_filters.FilterSet):
    start = django_filters.DateTimeFilter(field_name='created_at__date', lookup_expr='gte')
    end = django_filters.DateTimeFilter(field_name='created_at__date', lookup_expr='lte')
    action_taken = django_filters.BooleanFilter(method='action_filter')
    reporter_status = django_filters.CharFilter(method='reporter_action')
    hr_status = django_filters.CharFilter(method='hr_action')

    class Meta:
        model = Grievance
        fields = {
            'id': ['exact'],
            'user': ['exact'],
            'grievance_type': ['exact'],
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'is_approved': ['exact'],
            'is_rejected': ['exact'],
            'created_at': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'cancelled_date': ['exact', 'lt', 'lte', 'gt', 'gte']
        }

    def action_filter(self, queryset, name, value):
        return queryset.filter(is_approved=True) | queryset.filter(is_rejected=True)

    def reporter_action(self, queryset, name, value):
        if value == GRIEVANCE_REJECTED:
            return queryset.filter(grievance_HOD__is_rejected=True)
        elif value == GRIEVANCE_APPROVED:
            return queryset.filter(grievance_HOD__is_approved=True)
        elif value == GRIEVANCE_PENDING:
            return queryset.filter(is_cancelled=False, grievance_HOD__is_rejected=False,
                                   grievance_HOD__is_approved=False)
        else:
            return queryset

    def hr_action(self, queryset, name, value):
        if value == GRIEVANCE_REJECTED:
            return queryset.filter(grievance_HR__is_rejected=True)
        elif value == GRIEVANCE_APPROVED:
            return queryset.filter(grievance_HR__is_approved=True)
        elif value == GRIEVANCE_PENDING:
            return queryset.filter(is_cancelled=False, grievance_HR__is_rejected=False, grievance_HR__is_approved=False)
        else:
            return queryset
