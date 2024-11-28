from django.contrib.auth import get_user_model
from django.db import models
from .constants import employee_STATUS, BLOOD_GROUPS, ACTIVE
from ..base.models import TimeStampedModel


class DynamicSettings(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    icon = models.CharField(max_length=1024, blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_editable = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    is_deletable = models.BooleanField(default=True)

    class Meta:
        ordering = ['value']



class Country(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    country_code = models.CharField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class State(TimeStampedModel):
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=1024, blank=True, null=True)
    state_code = models.CharField(max_length=255, blank=True, null=True)
    is_territorial = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']


class City(TimeStampedModel):
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']


class Employee(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="employee_user")
    first_name = models.CharField(max_length=128, blank=True, null=True, default='')
    last_name = models.CharField(max_length=128, blank=True, null=True, default='')
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=128, blank=True, null=True, default='')
    mobile2 = models.CharField(max_length=128, blank=True, null=True, default='')
    designation = models.ForeignKey(DynamicSettings, blank=True, null=True, on_delete=models.PROTECT, related_name="employee_designation")
    department = models.ForeignKey(DynamicSettings, blank=True, null=True, on_delete=models.PROTECT, related_name="employee_department")
    emp_code = models.CharField(max_length=124, blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=employee_STATUS, default=ACTIVE, max_length=124, null=True)
    """documents"""
    aadhaar_no = models.CharField(max_length=1024, blank=True, null=True)
    pan_no = models.CharField(max_length=1024, blank=True, null=True)
    dl_no = models.CharField(max_length=1024, blank=True, null=True)
    passport = models.CharField(max_length=1024, blank=True, null=True)
    blood_group = models.CharField(choices=BLOOD_GROUPS, max_length=24, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
