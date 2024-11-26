import django_filters
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
            'is_aadhar_verified': ['exact'],
            'is_active': ['exact'],
        }

class CaseFilter(django_filters.FilterSet):

    class Meta:
        model = Grievance
        fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'prosecutor_lawyer' : ['exact', 'icontains'],
            'defender_lawyer': ['exact', 'icontains'],
            'accused_name': ['exact', 'icontains'],
            'victim_name': ['exact', 'icontains'],
            'status': ['exact'],
            'priority': ['exact'],
            'grievance_type': ['exact'],
            'employee': ['exact'],
            'accused': ['exact'],
            'victim': ['exact'],
            'user': ['exact'],
            'next_hearing_time': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'previous_hearing_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'next_hearing_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'created_at': ['exact', 'lt', 'lte', 'gt', 'gte']
        }
