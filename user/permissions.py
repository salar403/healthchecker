from rest_framework.permissions import BasePermission
from backend.customs.exceptions import CustomException

from user.models import User, Service


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, "customer", None)
        if not user or not isinstance(user, User) or not user.is_active:
            raise CustomException(code="unauthtenticated", status_code=401)
        return True


class IsServiceAuthtenticated(BasePermission):
    def has_permission(self, request, view):
        service = getattr(request, "service", None)
        if not service or not isinstance(service, Service) or not service.is_active:
            raise CustomException(code="unauthtenticated", status_code=401)
        return True
