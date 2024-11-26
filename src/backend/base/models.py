from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(_('modified'), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True
