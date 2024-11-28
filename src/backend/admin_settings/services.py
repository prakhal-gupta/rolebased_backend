import io
import re
import boto3
import zipfile
import logging
import random, string, requests

from django.conf import settings
from django.contrib.auth import get_user_model
from botocore.exceptions import ClientError
from ..accounts.serializers import UserSerializer
from ..base.utils.email import send_from_template
from decouple import config


def delete_child(parent_id, model_class):
    children = []
    if model_class.objects.filter(parent=parent_id, is_active=True).exists():
        query = model_class.objects.filter(parent=parent_id)
        for one in query:
            children.append(one.pk)
            delete_child(one.pk, model_class)
            one.is_active = False
            one.save()
        return children
    else:
        return children


def dropdown_tree(settings_list, serializer_class, model_class, parent_id=None, path=""):
    separator = "$#$"
    if len(settings_list) == 0:
        return []
    else:
        data = []
        for i in range(len(settings_list)):
            child = {
                **settings_list[i],
                'parent': parent_id,
                'path': path + separator + settings_list[i]['title'] if path else settings_list[i]['title'],
                'value': settings_list[i]['title'] + "-" + str(parent_id) if 'title' in settings_list[i] else ""
            }
            if len(child['children']) > 0:
                children = child['children']
                child['children'] = []
                queryset = model_class.objects.filter(name=child['title'], is_active=True)
                if parent_id:
                    queryset = queryset.filter(parent=parent_id)
                for item in queryset:
                    item_path = path + separator + child['path'] + separator + item.value if path else \
                        child['path'] + separator + item.value
                    child['children'].append({
                        'id': item.id,
                        'title': item.value,
                        'value': item.value + "-" + str(parent_id),
                        'path': item_path.split(separator),
                        'disabled': True,
                        'children': dropdown_tree(children, serializer_class, model_class, item.id, item_path)
                    })
            child['path'] = child['path'].split(separator)
            data.append(child)
        data.sort(key=lambda x: x.get('title'))
        return data


def generate_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def remove_special_characters(sting):
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', sting)


def generate_username(first_name=None, middle_name=None, last_name=None):
    first_name = first_name.replace(" ", "").replace(".", "") if first_name else first_name
    middle_name = middle_name.replace(" ", "").replace(".", "") if middle_name else middle_name
    last_name = last_name.replace(" ", "").replace(".", "") if last_name else last_name
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    if first_name:
        first_name = remove_special_characters(first_name)
        if len(first_name) > 4:
            return first_name[0:4].upper() + random_string
        if middle_name:
            middle_name = first_name + remove_special_characters(middle_name)
            if len(middle_name) > 4:
                return middle_name[0:4].upper() + random_string
        else:
            middle_name = ''
        if last_name:
            last_name = first_name + middle_name + remove_special_characters(last_name)
            if len(last_name) > 4:
                return last_name[0:4].upper() + random_string
        return first_name.upper() + random_string
    return None


def create_new_user(first_name=None, middle_name=None, last_name=None, email=None, mobile=None,
                    username=None, password=None, dob=None):
    user = get_user_model().objects.create(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                           email=email, mobile=mobile, username=username, dob=dob)
    password = generate_password() if not password else password
    user.set_password(password)
    user.save()
    return user, password


def create_employee(email=None, name=None, mobile=None):
    user = get_user_model().objects.filter(email=email, is_active=True).first()
    if not user:
        user, password = create_new_user(email=email, first_name=name, mobile=mobile)
        template = "employee_added.html"
        subject = "Your profile is added to a new Publisher"
        data = {
            'data': UserSerializer(user).data,
        }
        if password:
            subject = "Your profile has been created"
            template = "user_created.html"
            data['password'] = password
        send_from_template(user.email, subject, template, data)
    return user


def bulk_role(request_data):
    roles = request_data.get('roles', [])
    employees = request_data.get('employees', None)
    res_data = []
    for employee_id in employees:
        user = get_user_model().objects.filter(pk=employee_id, is_active=True).first()
        if user:
            record = {"id": user.id, "role": roles}
            res_data.append(record)
    return res_data
