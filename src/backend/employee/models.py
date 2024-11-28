from django.contrib.auth import get_user_model
from django.db import models
from ..accounts.models import Roles
from ..base.models import TimeStampedModel
from ..customer.models import Grievance


class GrievanceHODApproval(TimeStampedModel):
    grievance = models.ForeignKey(Grievance, blank=True, null=True, related_name='grievance_HOD',
                                  on_delete=models.PROTECT)
    action_by = models.ForeignKey(get_user_model(), blank=True, null=True, related_name='HOD_action_by',
                                  on_delete=models.PROTECT)
    action_date = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    remark = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-grievance__id']


class GrievanceHRApproval(TimeStampedModel):
    grievance = models.ForeignKey(Grievance, blank=True, null=True, related_name='grievance_HR',
                                  on_delete=models.PROTECT)
    approver = models.ForeignKey(Roles, blank=True, null=True, related_name='grievance_approver',
                                 on_delete=models.PROTECT)
    action_by = models.ForeignKey(get_user_model(), blank=True, null=True, related_name='HR_action_by',
                                  on_delete=models.PROTECT)
    action_date = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    remark = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-grievance__id']