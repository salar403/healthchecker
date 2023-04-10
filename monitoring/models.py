from django.db import models
from backend.customs.generators import current_int_timestamp

from user.models import User


class Endpoint(models.Model):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

    METHODS = [
        (GET, "get"),
        (POST, "post"),
        (PUT, "put"),
        (DELETE, "delete"),
    ]

    TEXT = 1
    JSON = 2
    ALL = 3

    VALID_TYPES = [
        (TEXT, "text"),
        (JSON, "json"),
        (TEXT, "all"),
    ]

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="endpoints",
        null=False,
    )
    name = models.CharField(max_length=500)
    base_url = models.URLField(null=False)
    method = models.IntegerField(choices=METHODS, null=False)
    response_type = models.IntegerField(choices=VALID_TYPES, default=JSON)
    headers = models.JSONField(null=True)
    body = models.JSONField(null=True)
    query_params = models.JSONField(null=True)
    healthy_status_code = models.IntegerField(default=200)
    required_result = models.JSONField(null=True)
    check_result_data = models.BooleanField(default=False)
    timeout = models.IntegerField(null=False)
    check_interval = models.IntegerField(null=False)
    recall_at = models.IntegerField(default=current_int_timestamp)
    convert_body_to_json = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class CallResult(models.Model):
    SUCCESS = 1
    TIMEOUT = 2
    INVALID_STATUS = 3
    ERROR = 4

    STATES = [
        (SUCCESS, "success"),
        (TIMEOUT, "timeout"),
        (INVALID_STATUS, "invalid_status"),
        (ERROR, "error"),
    ]

    endpoint = models.ForeignKey(
        to=Endpoint,
        on_delete=models.CASCADE,
        related_name="call_results",
        null=False,
    )
    timestamp = models.IntegerField(default=current_int_timestamp)
    response_time_ms = models.IntegerField(null=False)
    status_code = models.IntegerField(null=False)
    state = models.IntegerField(choices=STATES)
    healthy = models.BooleanField(null=False)
    error = models.TextField(null=True)
    result_json = models.JSONField(null=True)
    result_text = models.TextField(null=True)
