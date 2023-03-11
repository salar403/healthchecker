import json
from http.client import HTTPResponse
from django.utils.deprecation import MiddlewareMixin
from backend.services.login_manager import (
    validate_token,
    validate_api_key,
    service_ip_is_valid,
)


class CustomAuthorization(MiddlewareMixin):
    def reject(self, code: str, status: int = 401):
        return HTTPResponse(
            content=json.dumps({"code": code}),
            status=status,
            content_type="application/json",
        )

    def process_request(self, request):
        token = request.COOKIES.get("Bearer", None)
        key = request.COOKIES.get("Api-Key", None)
        if token and key:
            return self.reject(code="invalid_input")
        if not token and not key:
            return
        if token:
            session = validate_token(token=token)
            request.customer = session.user
            request.session_obj = session
        else:
            service = validate_api_key(api_key=key)
            if service_ip_is_valid(service=service, ip=request.ip):
                request.service = service
            return self.reject(code="invalid_ip", status=412)
