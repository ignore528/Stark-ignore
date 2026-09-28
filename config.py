# © @MuskanBot

import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()
API_ID = int(getenv("API_ID", "34766709"))
API_HASH = getenv("API_HASH", "c70063901bc81555174389982a394f95")
BOT_TOKEN = getenv("BOT_TOKEN", "8564248095:AAEYoF6YaYvZ5zsXb4aVjYk18p4rRVbdXV4")
OWNER_USERNAME = getenv("OWNER_USERNAME","sexydrifter")
BOT_USERNAME = getenv("BOT_USERNAME" , "DolbyMusicRobot")
BOT_NAME = getenv("BOT_NAME" , "DolbyAtoms")
ASSUSERNAME = getenv("ASSUSERNAME" , "")
BASE_URL = getenv("BASE_URL", "https://api.shrutibots.site")
API_KEY = getenv("API_KEY", "ShrutiBotsmz4lGsT87UWrai3SBsPK")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://deidaraasui12_db_user:lFMu0uvvRI5Kv86r@stark.yrjtl3r.mongodb.net/?appName=Stark")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
_logger_id_raw = getenv("LOGGER_ID", "0")
LOGGER_ID = int(_logger_id_raw) if _logger_id_raw and _logger_id_raw.lstrip("-1002488365579").isdigit() else 0
OWNER_ID = int(getenv("OWNER_ID", "7732395523"))
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Stark773/Paid-music",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None) or getenv("GITHUB_TOKEN", None)
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "http://t.me/textables")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "http://t.me/textables")
SOURCE = getenv("SOURCE", "https://t.me/sexydrifter")
CHAT = getenv("CHAT", "")
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))
STRING1 = getenv("STRING_SESSION", "AQISf3UAHxJ2ld_srxRWoB9XD7IPGHoqUvpkiNllSexSx06WtSlc_OzqhEC3dtumFwmekChIv_Nhz4pT4uCLLvdq0PW6fOyTw2-nl5J6tyOXwYyTWm6D6gxIO_1i9CXsHFwJMGH90kqwTR_kW44izEBd2UF2M9urNsAcW3ncKo7qWweOsDQzOA_64DY6H-OLQhVcsddX5pArwA1q9KvwKOOQ6NX2Eu3NiG7z8eVxFS7pQpffu5hpK4nkJ_9hRf3yLKh427OXWfxLWJhSm7v_3YR7SrrPm97Mt6l4P9sFzZPfUqDf8bApZU7CPsX558vMHoItvzpopkNuQQdj5OJVlq9B2bMBzAAAAAHfzIkMAA")
STRING2 = getenv("STRING_SESSION2", "")
STRING3 = getenv("STRING_SESSION3", "")
STRING4 = getenv("STRING_SESSION4", "")
STRING5 = getenv("STRING_SESSION5", "")
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
START_IMG_URL = getenv(
    "START_IMG_URL", "https://litter.catbox.moe/a9oxfp.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://litter.catbox.moe/a9oxfp.jpg"
)
PLAYLIST_IMG_URL = "https://litter.catbox.moe/a9oxfp.jpg"
STATS_IMG_URL = "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/c832e84cd991c865c7e4f.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/e575ae40d6635250974e1.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/03efec694e41e891b29dc.jpg"
IQ_Proxy = "https://i.ytimg.com/vi"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )

__all__ = [
    "IQ_Proxy",
]
