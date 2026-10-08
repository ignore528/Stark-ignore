# © @MuskanBot

import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# =========================
# TELEGRAM
# =========================

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")

OWNER_USERNAME = getenv("OWNER_USERNAME", "sexydrifter")
BOT_USERNAME = getenv("BOT_USERNAME", "DolbyMusicRobot")
BOT_NAME = getenv("BOT_NAME", "DolbyAtoms")

# Assistant / Userbot sessions
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", "")
STRING3 = getenv("STRING_SESSION3", "")
STRING4 = getenv("STRING_SESSION4", "")
STRING5 = getenv("STRING_SESSION5", "")

ASSUSERNAME = getenv("ASSUSERNAME", "")

# =========================
# API
# =========================

BASE_URL = getenv("BASE_URL", "")
API_KEY = getenv("API_KEY", "")

# =========================
# DATABASE
# =========================

MONGO_DB_URI = getenv("MONGO_DB_URI", "")

# =========================
# OWNER / LOGGER
# =========================

OWNER_ID = int(getenv("OWNER_ID", "0"))

_logger_id_raw = getenv("LOGGER_ID", "")
try:
    LOGGER_ID = int(_logger_id_raw.strip()) if _logger_id_raw.strip() else 0
except ValueError:
    LOGGER_ID = 0

# =========================
# HEROKU / GITHUB
# =========================

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/ignore528/Stark-ignore",
)

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

GIT_TOKEN = getenv("GIT_TOKEN", "") or getenv("GITHUB_TOKEN", "")

# =========================
# SUPPORT
# =========================

SUPPORT_CHANNEL = getenv(
    "SUPPORT_CHANNEL",
    "https://t.me/textables"
)

SUPPORT_CHAT = getenv(
    "SUPPORT_CHAT",
    "https://t.me/textables"
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
# MUSIC SETTINGS
# =========================

DURATION_LIMIT_MIN = int(
    getenv("DURATION_LIMIT", "17000")
)

SONG_DOWNLOAD_DURATION = int(
    getenv("SONG_DOWNLOAD_DURATION", "9999999")
)

SONG_DOWNLOAD_DURATION_LIMIT = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999")
)

PLAYLIST_FETCH_LIMIT = int(
    getenv("PLAYLIST_FETCH_LIMIT", "25")
)

TG_AUDIO_FILESIZE_LIMIT = int(
    getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000")
)

TG_VIDEO_FILESIZE_LIMIT = int(
    getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000")
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

# =========================
# IMAGES
# =========================

START_IMG_URL = getenv(
    "START_IMG_URL",
    "https://litter.catbox.moe/a9oxfp.jpg"
)

PING_IMG_URL = getenv(
    "PING_IMG_URL",
    "https://litter.catbox.moe/a9oxfp.jpg"
)

PLAYLIST_IMG_URL = getenv(
    "PLAYLIST_IMG_URL",
    "https://litter.catbox.moe/a9oxfp.jpg"
)

STATS_IMG_URL = getenv(
    "STATS_IMG_URL",
    "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg"
)

TELEGRAM_AUDIO_URL = getenv(
    "TELEGRAM_AUDIO_URL",
    "https://telegra.ph/file/c832e84cd991c865c7e4f.jpg"
)

TELEGRAM_VIDEO_URL = getenv(
    "TELEGRAM_VIDEO_URL",
    "https://telegra.ph/file/e575ae40d6635250974e1.jpg"
)

STREAM_IMG_URL = getenv(
    "STREAM_IMG_URL",
    "https://telegra.ph/file/03efec694e41e891b29dc.jpg"
)

SOUNCLOUD_IMG_URL = getenv(
    "SOUNCLOUD_IMG_URL",
    "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
)

YOUTUBE_IMG_URL = getenv(
    "YOUTUBE_IMG_URL",
    "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
)

SPOTIFY_ARTIST_IMG_URL = getenv(
    "SPOTIFY_ARTIST_IMG_URL",
    "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
)

SPOTIFY_ALBUM_IMG_URL = getenv(
    "SPOTIFY_ALBUM_IMG_URL",
    "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
)

SPOTIFY_PLAYLIST_IMG_URL = getenv(
    "SPOTIFY_PLAYLIST_IMG_URL",
    "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
)

IQ_Proxy = "https://i.ytimg.com/vi"

# =========================
# OTHER
# =========================

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# =========================
# DURATION
# =========================

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(stringt.split(":")))
    )

DURATION_LIMIT = int(
    time_to_seconds(f"{DURATION_LIMIT_MIN}:00")
)

# =========================
# URL VALIDATION
# =========================

if SUPPORT_CHANNEL:
    if not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. "
            "Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match(r"(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. "
            "Please ensure that it starts with https://"
        )

# =========================
# EXPORTS
# =========================

__all__ = [
    "IQ_Proxy",
]
