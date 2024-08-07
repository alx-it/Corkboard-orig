import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET = os.environ.get("SECRET")

TG_BOT_NAME = os.environ.get("TG_BOT_NAME")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
