from rest_framework.exceptions import ValidationError
from django.utils.encoding import force_str


class GrievanceValidationError(ValidationError):
    def __init__(self, detail):
        if isinstance(detail, dict) or isinstance(detail, list):
            self.detail = force_str(detail)
        else:
            self.detail = force_str(detail)
