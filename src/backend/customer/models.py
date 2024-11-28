from django.contrib.auth import get_user_model
from django.db import models
from ..base.models import TimeStampedModel
from ..admin_settings.models import State, City, DynamicSettings


class Customer(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="customer_user")
    name = models.CharField(max_length=1024, blank=True, null=True, default='')
    mobile = models.CharField(max_length=1024, blank=True, null=True, default='')
    email = models.CharField(max_length=1024, blank=True, null=True)
    father_name = models.CharField(max_length=1024, blank=True, null=True)
    aadhar_no = models.CharField(max_length=1024, blank=True, null=True)
    pan_no = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    pincode = models.CharField(max_length=254, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Grievance(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.PROTECT,
                             related_name="grievance_user")
    title = models.CharField(max_length=1024, blank=True, null=True)
    grievance_type = models.ForeignKey(DynamicSettings, blank=True, null=True, related_name='grievance_type',
                                       on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']