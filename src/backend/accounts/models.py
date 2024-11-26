from __future__ import unicode_literals
import logging
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .managers import PasswordResetCodeManager, UserManager
from ..base.models import TimeStampedModel
from ..base.utils import short_data

logger = logging.getLogger(__name__)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    first_name = models.CharField(max_length=128, blank=True, null=True, default='')
    middle_name = models.CharField(max_length=128, blank=True, null=True, default='')
    last_name = models.CharField(max_length=128, blank=True, null=True, default='')
    mobile = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    pan_no = models.CharField(max_length=255, null=True, blank=True, unique=True)
    username = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    date_joined = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_separated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email if self.email else self.username

    def get_short_name(self):
        return self.first_name or short_data.get_first_name(self.email)

    def get_full_name(self):
        full_name = self.first_name
        if self.middle_name:
            full_name += " " + self.middle_name
        if self.last_name:
            full_name += " " + self.last_name
        return full_name or ''


class AbstractBaseCode(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="User_Abstract", on_delete=models.PROTECT)
    code = models.CharField(_('code'), max_length=524, primary_key=True)
    uid = models.CharField(max_length=1024, default='uidrequired')
    timestamp = models.CharField(max_length=1024, default='timestamprequired')
    signature = models.CharField(max_length=1024, default='signaturerequired')

    class Meta:
        abstract = True

    def send_email(self, domain, is_publisher):
        PASSWORD_RESET_URL = domain + "/password-reset/"
        subject = "Reset Your Password"
        text_content = """Reset your password by clicking on this link:
                      %s{{ uid }}/{{ timestamp }}/{{ signature }}/{{  code }}
        """ % PASSWORD_RESET_URL
        from_email = settings.DEFAULT_EMAIL_FROM
        to = self.user.email
        ctxt = {
            'url': settings.PASSWORD_RESET_URL if not is_publisher else PASSWORD_RESET_URL,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'code': (self.code).decode(),
            'uid': self.uid,
            'timestamp': self.timestamp,
            'signature': self.signature

        }
        html_content = render_to_string('email/password_reset.html', ctxt)
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
        except Exception:
            logger.exception("Unable to send the mail.")

    def __unicode__(self):
        return "{0}, {1}, {2}, {3}".format(self.code, self.uid, self.timestamp, self.signature)


class PasswordResetCode(AbstractBaseCode):
    code = models.CharField(max_length=255)
    objects = PasswordResetCodeManager()

    def send_password_reset_email(self, domain, is_publisher):
        self.send_email(domain=domain, is_publisher=is_publisher)
