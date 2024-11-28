from collections import namedtuple
from functools import partial
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer, PasswordChangeSerializer, UserRegistrationSerializer
from ..admin_settings.models import Employee
from ..admin_settings.serializers import EmployeeSerializer
from ..base import response
from ..base.utils.email import send_from_template
from ..customer.models import Customer
from ..customer.serializers import CustomerSerializer

User = namedtuple('User', ['email', 'password'])


def _parse_data(data, cls):
    serializer = cls(data=data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    return serializer.validated_data

parse_auth_login_data = partial(_parse_data, cls=LoginSerializer)
parse_auth_password_change_data = partial(_parse_data, cls=PasswordChangeSerializer)
parse_register_user_data = partial(_parse_data, cls=UserRegistrationSerializer)


def employee_auth_data(request, user):
    token = get_tokens_for_user(user)
    login(request, user)
    auth_data = {
        "refresh": token.get('refresh'),
        "access": token.get('access'),
        "user": UserSerializer(instance=user, context={'request': request}).data,
    }
    return auth_data

def customer_auth_data(request, user):
    token = get_tokens_for_user(user)
    login(request, user)
    auth_data = {
        "refresh": token.get('refresh'),
        "access": token.get('access'),
        "user": UserSerializer(instance=user, context={'request': request}).data,
    }
    return auth_data


def auth_login(request):
    data, auth_data = parse_auth_login_data(request.data), None
    username, password = data.get('username'), data.get('password')
    if username and password:
        user, email_user, mobile_user, username_user = get_user_from_email_or_mobile_or_employee_code(username)
        if not user:
            return response.BadRequest({'detail': 'User does not exists.'})
        if user.is_separated:
            return response.BadRequest({'detail': 'User has been separated'})
        if user.check_password(password):
            if not user.is_active:
                return response.BadRequest({'detail': 'User account is disabled.'})
            if not user.is_superuser:
                return response.BadRequest({'detail': 'You are not an admin user!'})
            auth_data = generate_auth_data(request, user)
            return response.Ok(auth_data)
        else:
            if username_user:
                return response.BadRequest({'detail': 'Incorrect username and password.'})
            elif mobile_user:
                return response.BadRequest({'detail': 'Incorrect Mobile Number and password.'})
            else:
                return response.BadRequest({'detail': 'Incorrect Email and Password.'})
    else:
        return response.BadRequest({'detail': 'Must Include username and password.'})


def auth_login_employee(request):
    data, auth_data = parse_auth_login_data(request.data), None
    username, password = data.get('username'), data.get('password')
    if username and password:
        user, email_user, mobile_user, username_user = get_user_from_email_or_mobile_or_employee_code(username)
        if not user:
            return response.BadRequest({'detail': 'User does not exists.'})
        if user.is_separated:
            return response.BadRequest({'detail': 'User has been separated'})
        if user.check_password(password):
            if not user.is_active:
                return response.BadRequest({'detail': 'User account is disabled.'})
            employee_queryset = Employee.objects.filter(user=user.pk, is_active=True)
            if not employee_queryset.exists():
                return response.BadRequest({'detail': "You are not a employee!"})
            if employee_queryset.count() == 1 and employee_queryset.first().is_disabled:
                return response.BadRequest({'detail': 'Employee dashboard is disabled.'})
            auth_data = employee_auth_data(request, user)
            return response.Ok(auth_data)
        else:
            if username_user:
                return response.BadRequest({'detail': 'Incorrect username and password.'})
            elif mobile_user:
                return response.BadRequest({'detail': 'Incorrect Mobile Number and password.'})
            else:
                return response.BadRequest({'detail': 'Incorrect Email and Password.'})
    else:
        return response.BadRequest({'detail': 'Must Include username and password.'})


def auth_login_customer(request):
    data, auth_data = parse_auth_login_data(request.data), None
    username, password = data.get('username'), data.get('password')
    if username and password:
        user, email_user, mobile_user, username_user = get_user_from_email_or_mobile_or_employee_code(username)
        if not user:
            return response.BadRequest({'detail': 'User does not exists.'})
        if user.is_separated:
            return response.BadRequest({'detail': 'User has been separated'})
        if user.check_password(password):
            if not user.is_active:
                return response.BadRequest({'detail': 'User account is disabled.'})
            customer_query = Customer.objects.filter(user=user.pk, is_active=True)
            if not customer_query.exists():
                return response.BadRequest({'detail': "You are not a customer!"})
            auth_data = customer_auth_data(request, user)
            return response.Ok(auth_data)
        else:
            if username_user:
                return response.BadRequest({'detail': 'Incorrect username and password.'})
            elif mobile_user:
                return response.BadRequest({'detail': 'Incorrect Mobile Number and password.'})
            else:
                return response.BadRequest({'detail': 'Incorrect Email and Password.'})
    else:
        return response.BadRequest({'detail': 'Must Include username and password.'})


def auth_login_superuser(request):
    data = request.data.copy()
    username = data.get('username')
    if username:
        user, email_user, mobile_user, username_user = get_user_from_email_or_mobile_or_employee_code(username)
        if not user:
            return response.BadRequest({'detail': 'User does not exists.'})
        if not user.is_superuser:
            return response.BadRequest({'detail': 'You are not a superuser'})
        else:
            if not user.is_active:
                return response.BadRequest({'detail': 'User account is disabled.'})
            auth_data = generate_auth_data(request, user)
            return response.Ok(auth_data)
    else:
        return response.BadRequest({'detail': 'Must Include username.'})


def auth_password_change(request):
    data = parse_auth_password_change_data(request.data)
    return data


def auth_register_user(request):
    user_model = get_user_model()
    data = parse_register_user_data(request.data)
    user_data = User(
        email=data.get('email'),
        password=data.get('password')
    )
    user = None
    try:
        user = get_user_model().objects.get(email=data.get('email'), is_active=True)
    except get_user_model().DoesNotExist:
        pass
    if not user:
        un_active_user = user_model.objects.filter(email=user_data.email, is_active=False)
        if un_active_user:
            user_model.objects.filter(email=user_data.email, is_active=False).delete()
        user = user_model.objects.create_user(**dict(data), is_active=True)
        user.save()
    user_obj = user_model.objects.filter(email=data.get('email')).first()
    if user_obj:
        user_obj.set_password(data.get('password'))
        user_obj.save()
        subject = "Your profile has been created"
        template = "email/user_added.html"
        send_from_template(user.email, subject, template, data)
    return UserRegistrationSerializer(user).data


def get_user_from_email_or_mobile_or_employee_code(username):
    user_model = get_user_model()
    mobile_user = user_model.objects.filter(mobile__iexact=username, is_active=True).first()
    email_user = user_model.objects.filter(email__iexact=username, is_active=True).first()
    username_user = user_model.objects.filter(username__iexact=username, is_active=True).first()
    if email_user:
        user = email_user
    elif username_user:
        user = username_user
    else:
        user = mobile_user
    return user, email_user, username_user, mobile_user


def generate_auth_data(request, user):
    token = get_tokens_for_user(user)
    login(request, user)
    auth_data = {
        "refresh": token.get('refresh'),
        "access": token.get('access'),
        "user": UserSerializer(instance=user, context={'request': request}).data
    }
    return auth_data


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def user_clone_api(user, employee):

    auth_data = {
        "user": UserSerializer(instance=user).data,
        "employee_data": EmployeeSerializer(employee).data if employee else None
    }
    return auth_data

def customer_user_clone_api(user, customer):
    auth_data = {
        "user": UserSerializer(instance=user).data,
        "customer_user_data": CustomerSerializer(customer).data if customer else None
    }
    return auth_data

