# © @MuskanBot

import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


# =========================
# TELEGRAM
# =========================

API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

OWNER_ID = int(getenv("OWNER_ID", "0"))
OWNER_USERNAME = getenv("OWNER_USERNAME", "")

BOT_USERNAME = getenv("BOT_USERNAME", "")
BOT_NAME = getenv("BOT_NAME", "")


# =========================
# ASSISTANT SESSIONS
# =========================

STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", "")
STRING3 = getenv("STRING_SESSION3", "")
STRING4 = getenv("STRING_SESSION4", "")
STRING5 = getenv("STRING_SESSION5", "")


# =========================
# DATABASE
# =========================

MONGO_DB_URI = getenv("MONGO_DB_URI", "")


# =========================
# LOGGER
# =========================

_logger_id_raw = getenv("LOGGER_ID", "")

try:
    LOGGER_ID = int(_logger_id_raw)
except (ValueError, TypeError):
    LOGGER_ID = 0


# =========================
# BOT SETTINGS
# =========================

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "17000"))

ASSUSERNAME = getenv("ASSUSERNAME", "")

BASE_URL = getenv(
    "BASE_URL",
    "https://api.shrutibots.site"
)

API_KEY = getenv("API_KEY", "")


# =========================
# HEROKU / GITHUB
# =========================

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/ignore528/Stark-ignore"
)

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

GIT_TOKEN = getenv("GIT_TOKEN", "") or getenv("GITHUB_TOKEN", "")


# =========================
# SUPPORT
# =========================

SUPPORT_CHANNEL = getenv(
    "SUPPORT_CHANNEL",
    "http://t.me/textables"
)

SUPPORT_CHAT = getenv(
    "SUPPORT_CHAT",
    "http://t
