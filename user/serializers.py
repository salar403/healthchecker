from rest_framework import serializers

from backend.customs.exceptions import CustomException

from user.models import User
from backend.services.login_manager import login


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = User.objects.filter(username=data["username"], is_active=True)
        if not user.exists():
            raise CustomException(code="invalid_login")
        self.user = user.last()
        self.user.validate_password(password=data["password"])
        return data

    def create(self, validated_data):
        self._data = {"code": "success", "token": login(user=self.user)}
        return True
