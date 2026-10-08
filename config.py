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
    "http://t.me/textables"
)

SOURCE = getenv(
    "SOURCE",
    "https://t.me/sexydrifter"
)

CHAT = getenv("CHAT", "")


# =========================
# ASSISTANT SETTINGS
# =========================

AUTO_LEAVING_ASSISTANT = getenv(
    "AUTO_LEAVING_ASSISTANT",
    "False"
)

AUTO_LEAVE_ASSISTANT_TIME = int(
    getenv("ASSISTANT_LEAVE_TIME", "9000")
)


# =========================
# DOWNLOAD SETTINGS
# =========================

SONG_DOWNLOAD_DURATION = int(
    getenv("SONG_DOWNLOAD_DURATION", "9999999")
)

SONG_DOWNLOAD_DURATION_LIMIT = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999")
)


# =========================
# SPOTIFY
# =========================

SPOTIFY_CLIENT_ID = getenv(
    "SPOTIFY_CLIENT_ID",
    ""
)

SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET",
    ""
)

PLAYLIST_FETCH_LIMIT = int(
    getenv("PLAYLIST_FETCH_LIMIT", "25")
)


# =========================
# FILE SIZE LIMITS
# =========================

TG_AUDIO_FILESIZE_LIMIT = int(
    getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000")
)

TG_VIDEO_FILESIZE_LIMIT = int(
    getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000")
)


# =========================
# BANNED USERS
# =========================

BANNED_USERS = set()


# =========================
# OTHER SETTINGS
# =========================

YOUTUBE_DOWNLOAD_ATTEMPTS = int(
    getenv("YOUTUBE_DOWNLOAD_ATTEMPTS", "3")
)

COOKIE_URL = getenv("COOKIE_URL", "")

CLEANMODE = getenv("CLEANMODE", "False").lower() == "true"

PING_IMG = getenv("PING_IMG", "")

START_IMG_URL = getenv("START_IMG_URL", "")

HELP_IMG_URL = getenv("HELP_IMG_URL", "")

PLAY_IMG_URL = getenv("PLAY_IMG_URL", "")

SONG_IMG_URL = getenv("SONG_IMG_URL", "")

QUEUE_IMG_URL = getenv("QUEUE_IMG_URL", "")
