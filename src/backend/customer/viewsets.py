from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from .filters import CaseFilter, CustomerFilter
from .models import Grievance, Customer
from .permissions import CustomerPermissions
from .serializers import CaseSerializer, CustomerSerializer
from ..base import response
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from ..base.services import create_update_record


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = (CustomerPermissions,)
    parser_classes = (JSONParser, MultiPartParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(CustomerViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = CustomerFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Grievance.',
        operation_description='Add Grievance.',
        request_body=CaseSerializer,
        response=CaseSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Grievance.',
        operation_description='.',
        request_body=CaseSerializer,
        response=CaseSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Cases',
        operation_description='',
        response=CaseSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=Grievance, filterset_class=CaseFilter)
    def grievance(self, request):
        if request.method == "GET":
            queryset = Grievance.objects.filter(is_active=True)
            self.filterset_class = CaseFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CaseSerializer(page, many=True).data)
            return response.Ok(CaseSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CaseSerializer, Grievance))


    @swagger_auto_schema(
        method="put",
        operation_summary='Update Customer.',
        operation_description='.',
        request_body=CustomerSerializer,
        response=CustomerSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Customers',
        operation_description='',
        response=CustomerSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False, queryset=Customer, filterset_class=CustomerFilter)
    def customer(self, request):
        if request.method == "GET":
            queryset = Customer.objects.filter(is_active=True)
            self.filterset_class = CustomerFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CustomerSerializer(page, many=True).data)
            return response.Ok(CustomerSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CustomerSerializer, Customer))
