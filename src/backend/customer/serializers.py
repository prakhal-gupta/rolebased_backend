from datetime import datetime
from rest_framework import serializers
from .models import Customer, Grievance
from ..accounts.serializers import UserBasicDataSerializer
from ..admin_settings.serializers import EmployeeSerializer, DynamicSettingsDataSerializer
from ..base.serializers import ModelSerializer
from ..employee.models import GrievanceHODApproval, GrievanceHRApproval
from ..employee.serializers import GrievanceHODDataSerializer, GrievanceHRDataSerializer


class CustomerSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        instance = Customer.objects.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        Customer.objects.filter(id=instance.id).update(**validated_data)
        instance = Customer.objects.filter(id=instance.id).first()
        instance.save()
        return instance

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None


class GrievanceSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)
    grievance_type_data = serializers.SerializerMethodField(required=False)
    hod_data = serializers.SerializerMethodField(required=False)
    hr_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Grievance
        fields = '__all__'

    def create(self, validated_data):
        instance = Grievance.objects.create(**validated_data)
        instance.save()
        approval_data = {
            'grievance': instance,
            'is_active': True
        }
        GrievanceHODApproval.objects.create(**approval_data)
        return instance

    def update(self, instance, validated_data):
        user = validated_data.get('user', None)
        is_cancelled = validated_data.get('is_cancelled', None)
        if instance.is_cancelled:
            raise serializers.ValidationError({"detail": "This grievance is already cancelled"})
        if is_cancelled and instance.user == user:
            hod_data = GrievanceHODApproval.objects.filter(grievance=instance.id).first()
            if hod_data and (hod_data.is_approved or hod_data.is_rejected):
                raise serializers.ValidationError({"detail": "This grievance is already approved/rejected"})
            instance.is_cancelled = is_cancelled
            instance.cancelled_date = datetime.now()
            instance.save()
        else:
            raise serializers.ValidationError({"detail": "You can only cancel your grievance"})
        return instance

    @staticmethod
    def get_grievance_type_data(obj):
        return DynamicSettingsDataSerializer(obj.grievance_type).data if obj.grievance_type else None

    @staticmethod
    def get_hod_data(obj):
        hod_record = GrievanceHODApproval.objects.filter(grievance=obj.id, is_active=True).first()
        return GrievanceHODDataSerializer(hod_record).data if hod_record else None

    @staticmethod
    def get_hr_data(obj):
        hr_record = GrievanceHRApproval.objects.filter(grievance=obj.id, is_active=True).first()
        return GrievanceHRDataSerializer(hr_record).data if hr_record else None

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None
