from django.db.models import Q
from rest_framework import serializers
from .models import DynamicSettings, Country, State, City, Employee, EmployeePermissions
from .services import delete_child
from ..accounts.serializers import UserBasicDataSerializer
from ..base.serializers import ModelSerializer


class DynamicSettingsSerializer(ModelSerializer):
    class Meta:
        model = DynamicSettings
        fields = '__all__'

    def update(self, instance, validated_data):
        is_active = validated_data.get('is_active', True)
        if not is_active:
            delete_child(instance, DynamicSettings)
        DynamicSettings.objects.filter(is_active=True, id=instance.pk).update(**validated_data)
        instance = DynamicSettings.objects.filter(id=instance.pk).first()
        return instance


class DynamicSettingsDataSerializer(ModelSerializer):
    class Meta:
        model = DynamicSettings
        fields = ('id', 'value', 'icon', 'is_active')


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

    def validate(self, data):
        name = data.get('name', None)
        location = Country.objects.filter(name=name, is_active=True)
        if self.instance and self.instance.id:
            location = location.exclude(id=self.instance.id)
        if name and location.exists():
            raise serializers.ValidationError({"detail": "Country already exists."})
        return data


class StateBasicDataSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'state_code', 'is_territorial')


class StateSerializer(ModelSerializer):
    country_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = State
        fields = '__all__'

    def validate(self, data):
        name = data.get('name', None)
        location = State.objects.filter(name=name, is_active=True)
        if self.instance and self.instance.id:
            location = location.exclude(id=self.instance.id)
        if name and location.exists():
            raise serializers.ValidationError({"detail": "State already exists."})
        return data

    @staticmethod
    def get_country_data(obj):
        return CountrySerializer(obj.country).data if obj.country else None


class CityBasicDataSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'state')


class CitySerializer(ModelSerializer):
    state_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = City
        fields = '__all__'

    def validate(self, data):
        name = data.get('name', None)
        state = data.get('state', None)
        location = City.objects.filter(name=name, state=state, is_active=True)
        if self.instance and self.instance.id:
            location = location.exclude(id=self.instance.id)
        if name and location.exists():
            raise serializers.ValidationError({"detail": "City already exists."})
        return data

    @staticmethod
    def get_state_data(obj):
        return StateSerializer(obj.state).data if obj.state else None


class CountryBasicSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')


class StateBasicSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name',)


class CityBasicSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)


class DynamicSettingsValueSerializer(ModelSerializer):
    class Meta:
        model = DynamicSettings
        fields = ('value',)


class EmployeePermissionsSerializer(ModelSerializer):
    class Meta:
        model = EmployeePermissions
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    permissions = EmployeePermissionsSerializer(required=False, many=True)
    user_data = serializers.SerializerMethodField(required=False)
    designation_data = serializers.SerializerMethodField(required=False)
    department_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        court = data.get('court', None)
        user = data.get('user', None)
        first_name = data.get('first_name', None)
        queryset = Employee.objects.filter(court=court, is_active=True)
        queryset = queryset.filter(Q(user=user) | Q(first_name=first_name))
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError({"detail": "This user is already added."})
        return data

    def create(self, validated_data):
        instance = Employee.objects.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        Employee.objects.filter(id=instance.id).update(**validated_data)
        instance = Employee.objects.filter(id=instance.id).first()
        instance.save()
        return instance

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None

    @staticmethod
    def get_designation_data(obj):
        return DynamicSettingsDataSerializer(obj.designation, many=False).data if obj.designation else None

    @staticmethod
    def get_department_data(obj):
        return DynamicSettingsDataSerializer(obj.department, many=False).data if obj.department else None


class DeleteEmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'is_disabled', 'is_active')


class EmployeeListSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Employee
        fields = '__all__'

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None
