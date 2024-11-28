from datetime import datetime
from rest_framework import serializers
from ..accounts.models import Roles
from ..base.api.constants import HR_ROLE_SEED_DATA
from ..base.serializers import ModelSerializer
from .models import GrievanceHODApproval, GrievanceHRApproval
from ..accounts.serializers import UserBasicDataSerializer
from ..customer.models import Grievance

class GrievanceHODDataSerializer(ModelSerializer):
    class Meta:
        model = GrievanceHODApproval
        fields = '__all__'


class GrievanceHRDataSerializer(ModelSerializer):
    class Meta:
        model = GrievanceHRApproval
        fields = '__all__'


class GrievanceHODApprovalSerializer(ModelSerializer):
    grievance_data = serializers.SerializerMethodField(required=False)
    action_by_data = serializers.SerializerMethodField(required=False)
    hr_data = serializers.SerializerMethodField(required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = GrievanceHODApproval
        fields = '__all__'

    def update(self, instance, validated_data):
        is_approved = validated_data.get('is_approved', None)
        is_rejected = validated_data.get('is_rejected', None)
        grievance_obj = Grievance.objects.filter(id=instance.grievance.pk, is_active=True).first()
        hr_role = Roles.objects.filter(code_name=HR_ROLE_SEED_DATA["code_name"], is_active=True).first()
        if grievance_obj.is_cancelled:
            raise serializers.ValidationError({"detail": "This grievance is already cancelled"})
        if is_approved:
            grievance_obj.is_rejected = False
            grievance_obj.save()
            approval_data = {
                'grievance': grievance_obj,
                'approver': hr_role,
                'is_active': True
            }
            GrievanceHRApproval.objects.create(**approval_data)
        if is_rejected:
            grievance_obj.is_rejected = True
            grievance_obj.is_approved = False
            grievance_obj.save()
        validated_data["action_date"] = datetime.now()
        GrievanceHODApproval.objects.filter(id=instance.pk, is_active=True).update(**validated_data)
        instance = GrievanceHODApproval.objects.get(id=instance.pk)
        instance.save()
        return instance

    @staticmethod
    def get_grievance_data(obj):
        from ..customer.serializers import GrievanceSerializer
        return GrievanceSerializer(obj.grievance).data if obj.grievance else None

    @staticmethod
    def get_action_by_data(obj):
        return UserBasicDataSerializer(obj.action_by).data if obj.action_by else None

    @staticmethod
    def get_hr_data(obj):
        hr_record = GrievanceHRApproval.objects.filter(grievance=obj.grievance,
                                                       is_active=True).first() if obj.grievance else None
        return GrievanceHRDataSerializer(hr_record).data if hr_record else None


class GrievanceHRApprovalSerializer(ModelSerializer):
    grievance_data = serializers.SerializerMethodField(required=False)
    action_by_data = serializers.SerializerMethodField(required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = GrievanceHRApproval
        fields = '__all__'

    def update(self, instance, validated_data):
        is_approved = validated_data.get('is_approved', None)
        is_rejected = validated_data.get('is_rejected', None)
        grievance_obj = Grievance.objects.filter(id=instance.grievance.pk, is_active=True).first()
        if grievance_obj.is_cancelled:
            raise serializers.ValidationError({"detail": "This grievance is already cancelled"})
        if is_approved:
            grievance_obj.is_approved = True
            grievance_obj.is_rejected = False
        if is_rejected:
            grievance_obj.is_rejected = True
            grievance_obj.is_approved = False
        grievance_obj.save()
        validated_data["action_date"] = datetime.now()
        GrievanceHRApproval.objects.filter(id=instance.pk, is_active=True).update(**validated_data)
        instance = GrievanceHRApproval.objects.get(id=instance.pk)
        instance.save()
        return instance

    @staticmethod
    def get_grievance_data(obj):
        from ..customer.serializers import GrievanceSerializer
        return GrievanceSerializer(obj.grievance).data if obj.grievance else None

    @staticmethod
    def get_action_by_data(obj):
        return UserBasicDataSerializer(obj.action_by).data if obj.action_by else None
