from rest_framework import serializers

from backend.customs.exceptions import CustomException

from user.models import User
from backend.services.login_manager import login


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        admin = User.objects.filter(username=data["username"], is_active=True)
        if not admin.exists():
            raise CustomException(code="invalid_login")
        self.admin = admin.last()
        self.admin.validate_password(password=data["password"])
        return data

    def create(self, validated_data):
        self._data = {"code": "success", "token": login(admin=self.admin)}
        return True
