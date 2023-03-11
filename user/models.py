from django.db import models
from hashlib import sha3_512
from backend.customs.exceptions import CustomException

from backend.customs.generators import (
    generate_salt,
    generate_session_key,
    generate_session_expiration,
)
from backend.settings import PASSWORD_HASHING_ITERATIONS


class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=1000, null=True)
    salt = models.CharField(
        max_length=100,
        default=generate_salt,
        null=False,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def generate_password_hash(self, password):
        password_hash = f"{password}{self.salt}"
        for _ in range(PASSWORD_HASHING_ITERATIONS):
            password_hash = sha3_512(password_hash.encode()).hexdigest()
        return password_hash

    def validate_password(self, password: str):
        if self.password == self.generate_password_hash(password=password):
            return True
        raise CustomException(code="invalid_login")

    def set_password(self, password: str):
        self.password = self.generate_password_hash(password=password)
        self.save()


class Session(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name="sessions",
        on_delete=models.CASCADE,
        null=False,
    )
    key = models.CharField(max_length=200, default=generate_session_key)
    valid_time = models.BigIntegerField(default=generate_session_expiration)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Service(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name="services",
        on_delete=models.CASCADE,
        null=False,
    )
    api_key_hash = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ValidServiceIp(models.Model):
    class Meta:
        unique_together = ("ip","service")
    ip = models.GenericIPAddressField(null=False)
    service = models.ForeignKey(
        to=Service,
        related_name="valid_ips",
        on_delete=models.CASCADE,
        null=False,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
