from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import User
from ..base.serializers import ModelSerializer
from ..customer.models import Customer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name', 'mobile', 'is_staff',
            'is_active', 'is_superuser', 'is_separated', 'date_joined', 'dob'
        )
        extra_kwargs = {'password': {'write_only': True}, 'last_login': {'read_only': True},
                        'is_superuser': {'read_only': True}}


class UserBasicDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'username', 'mobile', 'dob', 'is_active')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField( allow_blank=False, allow_null=False,
        error_messages={'required': 'Please enter a valid mobile/email id.',
                        'blank': 'Please enter a valid mobile/email id.',
                        'null': 'Please enter a valid mobile/email id.'}
    )
    password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(min_length=8,  max_length=128,
        error_messages={'required': 'Please enter a valid password.',
                        'blank': 'Please enter a valid password.',
                        'null': 'Please enter a valid password.',
                        'min_length': 'Password should have minimum 8 characters.'}
    )


class UserRegistrationSerializer(ModelSerializer):

    email = serializers.EmailField(  allow_blank=False, allow_null=False,
        error_messages={
            'required': 'Please enter a valid e-mail id.',
            'invalid': 'Please enter a valid e-mail id.',
            'blank': 'Please enter a valid e-mail id.',
            'null': 'Please enter a valid e-mail id.'
        },
    )

    class Meta:
        model = get_user_model()
        fields = (
        'id', 'email', 'mobile', "password", 'first_name', 'middle_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def validate_password(self, value):
        if len(value) > 7:
            return value
        else:
            msg = _('Password should have minimum 8 characters.')
            raise serializers.ValidationError(msg)


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(  allow_blank=False,  allow_null=False,
        error_messages={'required': 'Please enter a valid mobile.',
                        'blank': 'Please enter a valid mobile.',
                        'null': 'Please enter a valid mobile'})
    is_employee = serializers.BooleanField(required=False)


class CustomerRegistrationSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def validate(self, data):
        aadhar_no = data.get('aadhar_no', None)
        email = data.get('email', None)
        if aadhar_no:
            if Customer.objects.filter(aadhar_no=aadhar_no, is_active=True).exists():
                raise serializers.ValidationError({"aadhar_no": "A user with this Aadhar number already exists."})
        if email:
            if Customer.objects.filter(email=email, is_active=True).exists():
                raise serializers.ValidationError({"email": "A user with this email already exists."})
        return data

    def create(self, validated_data):
        instance = Customer.objects.create(**validated_data)
        instance.save()
        return instance

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None