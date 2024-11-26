from rest_framework import serializers
from .models import Customer, Grievance
from ..accounts.serializers import UserBasicDataSerializer
from ..admin_settings.serializers import EmployeeSerializer
from ..base.serializers import ModelSerializer


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


class CaseSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)
    victim_data = serializers.SerializerMethodField(required=False)
    accused_data = serializers.SerializerMethodField(required=False)
    employee_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Grievance
        fields = '__all__'

    @staticmethod
    def get_victim_data(obj):
        return CustomerSerializer(obj.victim).data if obj.victim else None

    @staticmethod
    def get_accused_data(obj):
        return CustomerSerializer(obj.accused).data if obj.accused else None

    @staticmethod
    def get_employee_data(obj):
        return EmployeeSerializer(obj.employee).data if obj.employee else None

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None
