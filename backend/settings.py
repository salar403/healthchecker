from pathlib import Path

from backend.environments import (
    API_HOST,
    BACKEND_POSTGRES_HOST,
    BACKEND_POSTGRES_NAME,
    BACKEND_POSTGRES_PASSWORD,
    BACKEND_POSTGRES_PORT,
    BACKEND_POSTGRES_USERNAME,
    BACKEND_REDIS_HOST,
    BACKEND_REDIS_PORT,
    PLATFORM,
    REDIS_CACHE_LOCK,
    REDIS_CELERY_BACKEND,
    REDIS_CELERY_BROKER,
    REDIS_DEFAULT,
    REDIS_RATELIMIT,
    REDIS_TRY_RATE,
    SWAGGER_URL,
    PROJECT_SECRET_KEY,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = PROJECT_SECRET_KEY

DEBUG = bool(PLATFORM != "production")

ALLOWED_HOSTS = [API_HOST]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "user",
    "monitoring",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "backend.middlewares.common.CommonMiddleware",
    "backend.middlewares.authorization.CustomAuthorization",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": BACKEND_POSTGRES_NAME,
        "USER": BACKEND_POSTGRES_USERNAME,
        "PASSWORD": BACKEND_POSTGRES_PASSWORD,
        "HOST": BACKEND_POSTGRES_HOST,
        "PORT": BACKEND_POSTGRES_PORT,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_DEFAULT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "ratelimit": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_RATELIMIT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "cache_lock": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CACHE_LOCK}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "try_rate": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_TRY_RATE}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

CELERY_BROKER_URL = (
    f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CELERY_BROKER}"
)
CELERY_RESULT_BACKEND = (
    f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CELERY_BACKEND}"
)
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 31540000}
CELERY_CREATE_MISSING_QUEUES = True

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Key": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_API_URL": SWAGGER_URL,
}
PASSWORD_HASHING_ITERATIONS = 750


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
    },
}

REQUEST_RATE_1MIN = 100
REQUEST_RATE_15MIN = 500
REQUEST_RATE_1HOUR = 1000
REQUEST_BLOCK_RATE = 100
CDN_BLOCKING_RATE = 100
