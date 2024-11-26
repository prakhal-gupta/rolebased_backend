import re
from ..api.exceptions import LawsphereValidationError
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class NameValidator(object):
    valid_message = _('Please enter a valid Name.')

    def __call__(self, value):
        if re.match("^[a-zA-Z]+[a-zA-Z. ]*$", value):
            return value
        else:
            raise LawsphereValidationError(self.valid_message)


class MobileValidator(object):
    valid_message = _('Please enter a valid mobile number')
    valid_number_message = _('Please enter a valid mobile number')
    number_exceed_message = _('Mobile number length must be 10 digits')
    valid_number_start_message = _('Mobile number must starting with 6 or 7 or 8 or 9')

    def __call__(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(self.valid_message)
        except TypeError:
            raise ValidationError(self.valid_number_message)

        if str(value)[0] not in ('6', '7', '8', '9'):
            raise ValidationError(self.valid_number_start_message)

        if len(str(value)) != 10:
            raise ValidationError(self.valid_number_message)
