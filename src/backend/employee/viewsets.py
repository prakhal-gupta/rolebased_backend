from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from ..base import response
from ..base.api.constants import HR_ROLE_SEED_DATA
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from ..base.services import create_update_record
from ..accounts.models import Roles
from ..admin_settings.serializers import EmployeeSerializer
from ..admin_settings.filters import EmployeeFilter
from ..admin_settings.models import Employee
from .filters import GrievanceHODApprovalFilter, GrievanceHRApprovalFilter
from .models import GrievanceHODApproval, GrievanceHRApproval
from .permissions import EmployeePermissions
from .serializers import GrievanceHODApprovalSerializer, GrievanceHRApprovalSerializer


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = (EmployeePermissions,)
    parser_classes = (JSONParser, MultiPartParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(EmployeeViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = EmployeeFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @swagger_auto_schema(
        method="put",
        operation_summary='HOD Approval',
        operation_description='Used to approve grievances by HOD.',
        request_body=GrievanceHODApprovalSerializer,
        response=GrievanceHODApprovalSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Grievances',
        operation_description='Returns all the grievance for given HOD. action_taken used as key to send result as per HOD',
        response=GrievanceHODApprovalSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False, queryset=GrievanceHODApproval, filterset_class=GrievanceHRApprovalFilter)
    def hod_approval(self, request):
        if request.method == "GET":
            action_taken = request.query_params.get('action_taken', None)
            queryset = GrievanceHODApproval.objects.filter(grievance__is_cancelled=False, grievance__is_active=True,
                                                           is_active=True)
            if action_taken is None:
                queryset = queryset.none()
            self.filterset_class = GrievanceHODApprovalFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(GrievanceHODApprovalSerializer(page, many=True).data)
            return response.Ok(GrievanceHODApprovalSerializer(queryset, many=True).data)
        else:
            request_data = request.data.copy()
            request_data['action_by'] = request.user.pk
            existing_approval = GrievanceHODApproval.objects.filter(grievance_id=request.data.get('grievance')).first()
            if existing_approval:
                request_data['id'] = existing_approval.id
            else:
                return response.BadRequest({"detail": "No GrievanceHODApproval record found for the given grievance."})
        return response.Ok(create_update_record(request_data, GrievanceHODApprovalSerializer, GrievanceHODApproval))

    @swagger_auto_schema(
        method="put",
        operation_summary='HR Approval',
        operation_description='Used to approve grievances by HR.',
        request_body=GrievanceHRApprovalSerializer,
        response=GrievanceHRApprovalSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Grievances',
        operation_description='Returns all the grievance for given HR. action_taken used as key to send result as per HR',
        response=GrievanceHRApprovalSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False, queryset=GrievanceHRApproval, filterset_class=GrievanceHRApprovalFilter)
    def hr_approval(self, request):
        if request.method == "GET":
            action_taken = request.query_params.get('action_taken', None)
            role_code = request.query_params.get('role', None)
            role_obj = Roles.objects.filter(code_name=role_code).first()
            queryset = GrievanceHRApproval.objects.filter(grievance__is_cancelled=False, is_active=True)
            if action_taken is None:
                queryset = queryset.none()
            role = request.user.role.values_list('id', flat=True)
            if role_obj:
                if role_code == HR_ROLE_SEED_DATA["code_name"]:
                    queryset = queryset.filter(approver=role_obj) | queryset.filter(approver__isnull=True)
                else:
                    queryset = queryset.filter(approver=role_obj)
            else:
                queryset = queryset.filter(approver__in=role)
            self.filterset_class = GrievanceHRApprovalFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(GrievanceHRApprovalSerializer(page, many=True).data)
            return response.Ok(GrievanceHRApprovalSerializer(queryset, many=True).data)
        else:
            request_data = request.data.copy()
            request_data['action_by'] = request.user.pk
            existing_approval = GrievanceHRApproval.objects.filter(grievance_id=request.data.get('grievance')).first()
            if existing_approval:
                request_data['id'] = existing_approval.id
            else:
                return response.BadRequest({"detail": "No GrievanceHRApproval record found for the given grievance."})
            return response.Ok(create_update_record(request_data, GrievanceHRApprovalSerializer, GrievanceHRApproval))
