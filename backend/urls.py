from backend.settings import SWAGGER_SETTINGS
from django.urls import path, re_path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.staticfiles.views import serve


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path("user/", include("user.urls")),
    path("monitoring/", include("monitoring.urls")),
    # path("telegram/", include("user.urls", namespace="secret")),
]
swagger_urls = [
    item
    for item in urlpatterns
    if hasattr(item, "namespace") and item.namespace != "secret"
]

schema_view = get_schema_view(
    openapi.Info(
        title="HealthCheck API",
        default_version="v1.0",
        description="HealthCheck Backend",
        contact=openapi.Contact(email="salar40340@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=SWAGGER_SETTINGS["DEFAULT_API_URL"],
    patterns=swagger_urls,
)
urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^static/(?P<path>.*)$", return_static, name="static"),
]
