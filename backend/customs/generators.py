import time, secrets
from uuid import uuid4
from hashlib import sha3_512


def generate_uuid():
    return str(uuid4())


def generate_salt(nbytes: int = 40):
    return secrets.token_urlsafe(nbytes=nbytes)


def generate_password():
    return secrets.token_urlsafe(16)


def generate_session_key(nbytes=64):
    return generate_salt(nbytes=nbytes)


def generate_session_expiration(valid_window: int = 60 * 60 * 8):
    return int(time.time() + valid_window)


def generate_api_key():
    key = secrets.token_urlsafe(40)
    key_hash = sha3_512(key.encode()).hexdigest()
    return key, key_hash
