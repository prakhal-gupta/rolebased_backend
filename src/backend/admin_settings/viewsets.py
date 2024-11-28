from decouple import config
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from .constants import SETTINGS_CONSTANT
from .filters import DynamicSettingsFilter, CountryFilter, StateFilter, CityFilter,  EmployeeFilter
from .models import DynamicSettings, Country, State, City, Employee
from .permissions import DynamicSettingsPermissions
from .serializers import (DynamicSettingsSerializer, CountrySerializer, StateSerializer, CitySerializer,
                          DeleteEmployeeSerializer, EmployeeSerializer)
from .services import dropdown_tree, create_new_user, bulk_role
from ..accounts.filters import UserBasicFilter, RolesFilter
from ..accounts.models import Roles
from ..accounts.serializers import UserSerializer, RoleSerializer
from ..base.utils.email import send_from_template
from ..base import response
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from ..base.services import create_update_record, create_update_bulk_records


class DynamicSettingsViewSet(ModelViewSet):
    serializer_class = DynamicSettingsSerializer
    queryset = DynamicSettings.objects.all()
    permission_classes = (DynamicSettingsPermissions,)
    parser_classes = (JSONParser, MultiPartParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(DynamicSettingsViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = DynamicSettingsFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @swagger_auto_schema(
        method="get",
        operation_summary='List of dynamic settings',
        operation_description='Admin can get list of all dynamic settings',
        response=DynamicSettingsSerializer
    )
    @action(methods=['GET'], detail=False)
    def dropdown(self, request):
        dropdown_list = SETTINGS_CONSTANT
        data = dropdown_tree(dropdown_list, DynamicSettingsSerializer, DynamicSettings)
        return response.Ok(data)

    @swagger_auto_schema(
        method="put",
        operation_summary='Update User Storage.',
        operation_description='.',
        request_body=UserSerializer,
        response=UserSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of user storage',
        operation_description='',
        response=UserSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False)
    def users(self, request):
        if request.method == "GET":
            queryset = get_user_model().objects.filter(is_active=True)
            self.filterset_class = UserBasicFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(UserSerializer(page, many=True).data)
            return response.Ok(UserSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, UserSerializer, get_user_model()))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Country',
        operation_description='Add Country',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Country.',
        operation_description='.',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Country',
        operation_description='',
        response=CountrySerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=Country, filterset_class=CountryFilter)
    def country(self, request):
        if request.method == "GET":
            queryset = Country.objects.filter(is_active=True)
            self.filterset_class = CountryFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CountrySerializer(page, many=True).data)
            return response.Ok(CountrySerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CountrySerializer, Country))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add State',
        operation_description='Add State',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update State.',
        operation_description='.',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of State',
        operation_description='',
        response=CountrySerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=State, filterset_class=StateFilter)
    def state(self, request):
        if request.method == "GET":
            queryset = State.objects.filter(is_active=True)
            self.filterset_class = StateFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(StateSerializer(page, many=True).data)
            return response.Ok(StateSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, StateSerializer, State))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add City',
        operation_description='Add City',
        request_body=CitySerializer,
        response=CitySerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update City.',
        operation_description='.',
        request_body=CitySerializer,
        response=CitySerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of City',
        operation_description='',
        response=CitySerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=City, filterset_class=CityFilter)
    def city(self, request):
        if request.method == "GET":
            queryset = City.objects.filter(is_active=True)
            self.filterset_class = CityFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CitySerializer(page, many=True).data)
            return response.Ok(CitySerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CitySerializer, City))


    @swagger_auto_schema(
        method="post",
        operation_summary='Add Employee.',
        operation_description='Add Employee.',
        request_body=EmployeeSerializer,
        response=EmployeeSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Employee.',
        operation_description='.',
        request_body=EmployeeSerializer,
        response=EmployeeSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Employee',
        operation_description='',
        response=EmployeeSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=Employee,
            filterset_class=EmployeeFilter)
    def employee(self, request):
        if request.method == "GET":
            queryset = Employee.objects.filter(court__is_active=True, is_active=True)
            self.filterset_class = EmployeeFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(EmployeeSerializer(page, many=True).data)
            return response.Ok(EmployeeSerializer(queryset, many=True).data)
        else:
            request_data = request.data.copy()
            id = request_data.get("id", None)
            email = request_data.get("email", None)
            mobile = request_data.get("mobile", None)
            first_name = request_data.get("first_name", None)
            last_name = request_data.get("last_name", None)
            if not id:
                if not email:
                    return response.BadRequest({"detail": "Email is required!"})
            user = get_user_model().objects.filter(email=email, is_active=True).first()
            if not user:
                user, password = create_new_user(email=email, mobile=mobile, first_name=first_name, last_name=last_name)
                template = "employee_added.html"
                subject = "Your profile is added to Grievance Management"
                data = {
                    'data': UserSerializer(user).data,
                    'login_link': config('DOMAIN')
                }
                if password:
                    subject = "Your profile has been created on Grievance Management."
                    template = "user_created.html"
                    data['password'] = password
                    data['professional_name'] = user.first_name if user.first_name else '--'
                    data['mobile'] = user.mobile if user.mobile else '--'
                    send_from_template(user.email, subject, template, data)
                elif not id:
                    send_from_template(user.email, subject, template, data)
                    if user.mobile:
                        name = user.first_name if user.first_name else "User"
            request_data['user'] = user.pk
            return response.Ok(create_update_record(request_data, EmployeeSerializer, Employee))

    @swagger_auto_schema(
        method="put",
        operation_summary='For disabling and deleting employee',
        operation_description='',
        request_body=DeleteEmployeeSerializer,
        response=EmployeeSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Deleted EmployeeS',
        operation_description='',
        response=EmployeeSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False, queryset=Employee, filterset_class=EmployeeFilter)
    def deleted_employee(self, request):
        if request.method == 'GET':
            queryset = Employee.objects.filter(is_active=False)
            self.filterset_class = EmployeeFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(EmployeeSerializer(page, many=True).data)
            return response.Ok(EmployeeSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, DeleteEmployeeSerializer, Employee))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Roles',
        operation_description='',
        request_body=RoleSerializer,
        response=RoleSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Roles',
        operation_description='.',
        request_body=RoleSerializer,
        response=RoleSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Roles',
        operation_description='',
        response=RoleSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, pagination_class=StandardResultsSetPagination, queryset=Roles,
            filterset_class=RolesFilter)
    def role(self, request):
        if request.method == "GET":
            queryset = Roles.objects.filter(is_active=True)
            self.filterset_class = RolesFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(RoleSerializer(page, many=True).data)
            return response.Ok(RoleSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, RoleSerializer, Roles))


    @swagger_auto_schema(
        method="post",
        operation_summary='Add Employee Role',
        operation_description='Add Employee Role',
        request_body=UserSerializer,
        response=UserSerializer
    )
    @action(methods=['POST'], detail=False, pagination_class=StandardResultsSetPagination)
    def bulk_employee_role_edit(self, request):
        request_data = request.data.copy()
        records = bulk_role(request_data)
        result = create_update_bulk_records(records, UserSerializer, get_user_model())
        if result["success"]:
            return response.Ok(result["data"])
        else:
            return response.BadRequest(result["errors"])
