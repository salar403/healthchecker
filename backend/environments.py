from os import getenv

PLATFORM = getenv("PLATFORM", "local")
SWAGGER_URL = getenv("SWAGGER_URL", "http://127.0.0.1:8000")
BOT_TOKEN = getenv("BOT_TOKEN", "")
