from ..admin_settings.models import Employee


def get_employee_obj(user):
    if user:
        employee_obj = Employee.objects.filter(user=user, is_active=True).first()
        if employee_obj:
            return employee_obj
        else:
            raise ValueError('Invalid Employee')
    return None
