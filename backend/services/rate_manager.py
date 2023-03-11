import time
from django.core.cache import caches

from backend.settings import (
    CDN_BLOCKING_RATE,
    REQUEST_RATE_1MIN,
    REQUEST_RATE_15MIN,
    REQUEST_RATE_1HOUR,
    REQUEST_BLOCK_RATE,
)
from backend.customs.exceptions import CustomException

cache = caches["ratelimit"]
try_rate_cache = caches["try_rate"]


def check_interval_override(
    ip: str,
    interval_name: str,
    interval_seconds: int,
    rate_count: int,
):
    rate = len(cache.keys(f"{ip}_{interval_name}_*"))
    if rate >= rate_count:
        return True
    cache.set(f"{ip}_{interval_name}_{time.time()}", True, interval_seconds)
    return False


def has_overrided_intervals(ip: str):
    interval_map = {
        "1hour": [60 * 60, REQUEST_RATE_1HOUR],
        "15min": [15 * 60, REQUEST_RATE_15MIN],
        "1min": [60, REQUEST_RATE_1MIN],
    }
    for interval_name in interval_map:
        overrided = check_interval_override(
            ip=ip,
            interval_name=interval_name,
            interval_seconds=interval_map[interval_name][0],
            rate_count=interval_map[interval_name][1],
        )
        if overrided:
            return True
    return False


def check_blocked(ip: str):
    key = f"{ip}_blocked"
    blocked_count = cache.get(key)
    if not blocked_count:
        return False
    if blocked_count <= CDN_BLOCKING_RATE:
        cache.incr(key)
    return True


def block_ip_from_backend(ip: str):
    cache.set(f"{ip}_blocked", 1, 60 * 60 * 6)



def check_blocking_limit(ip: str):
    rate = len(cache.keys(f"{ip}_block_*"))
    if rate <= REQUEST_BLOCK_RATE:
        cache.set(f"{ip}_block_{time.time()}", True, 60 * 60)
    else:
        block_ip_from_backend(ip=ip)


def ip_is_limited(ip: str):
    if check_blocked(ip):
        return True
    if not has_overrided_intervals(ip):
        return False
    check_blocking_limit(ip)
    return True


def try_rate_limit(
    identifier: str,
    max_trys: int = 3,
    expiration: int = 60,
    set_try: bool = False,
):
    try_count = len(try_rate_cache.keys(f"{identifier}_*"))
    if try_count > max_trys:
        return True
    if set_try:
        try_rate_cache.set(f"{identifier}_{time.time()}", True, expiration)
    return False


def check_password_ratelimit(identifier: str):
    if try_rate_limit(identifier=identifier):
        raise CustomException(code="maximum_trys_reached")


def add_wrong_password_try(identifier: str):
    try_rate_limit(identifier=identifier, set_try=True)
