from os import getenv

PLATFORM = getenv("PLATFORM", "local")
SWAGGER_URL = getenv("SWAGGER_URL", "http://127.0.0.1:8000")
BOT_TOKEN = getenv("BOT_TOKEN", "")
SECRET_KEY = getenv("SECRET_KEY","django-insecure-w009)3tg7g**m=)v3%op^)6m3wf0a#hw0-7dff$%-_l*C%68SE")