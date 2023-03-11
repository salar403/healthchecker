import json
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import caches

from backend.services.rate_manager import ip_is_limited
from backend.settings import DEBUG

cache = caches["default"]


def response(code: str, status: int):
    return HttpResponse(
        content=json.dumps({"code": code}),
        status=status,
        content_type="application/json",
    )


class CommonMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not DEBUG:
            ip = request.headers.get("CF-Connecting-IP", None)
            pseudo_ip = request.headers.get("Cf-Pseudo-IPv4", None)
            country = request.headers.get("CF-IPCountry", None)
        else:
            ip = request.META.get("REMOTE_ADDR", None)
            pseudo_ip = None
            country = "LOCAL"
        user_agent = request.headers.get("User-Agent", None)
        request.ip = ip
        if not ip:
            return response(code="forbidden", status=403)
        if ip_is_limited(ip=ip):
            return response(code="limited", status=429)
        if not user_agent:
            return response(code="invalid_user_agent", status=403)
        request.country = country
        request.device = user_agent
        request.pseudo_ip = pseudo_ip

    def process_response(self, request, response):
        if 400 <= response.status_code < 500:
            for _ in range(9):
                ip_is_limited(ip=request.ip)
        return response
