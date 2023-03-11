from rest_framework import serializers

from backend.customs.exceptions import CustomException
from backend.customs.generators import generate_api_key

from user.models import User, Service
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


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "is_active", "created_at"]
        model = Service


class AddServiceSerizlier(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate_name(self, name):
        user = self.context["user"]
        if user.services.filter(is_active=True, name=name).exists():
            raise CustomException(code="duplicated_service_name")
        return name

    def create(self, validated_data):
        service = Service.objects.create(
            user=self.context["user"], name=validated_data["name"]
        )
        api_key, api_key_hash = generate_api_key()
        service.api_key_hash = api_key_hash
        service.save()
        data = ServiceSerializer(service).data
        data["api_key"] = api_key
        self._data = {"code": "success", "data": data}
        return super().create(validated_data)
