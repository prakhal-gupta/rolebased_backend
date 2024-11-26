from ..accounts.models import User
from ..base.serializers import ModelSerializer


class UserEmployeeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'dob', 'last_login')
