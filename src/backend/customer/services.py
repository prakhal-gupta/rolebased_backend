from ..customer.models import Customer


def get_customer_user_obj(user):
    if user:
        customer_user_obj = Customer.objects.filter(user=user, is_active=True).first()
        if customer_user_obj:
            return customer_user_obj
        else:
            raise ValueError('Invalid User')
    return None
