from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "unknown_error"

    def __init__(self, detail=None, code=None, status_code=None):
        if code is None:
            code = self.default_code
        if status_code is not None:
            self.status_code = status_code

        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = detail
        if detail:
            self.detail = {"code": code, "message": detail}
        else:
            self.detail = {"code": code}
