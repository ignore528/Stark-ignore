# Â© @MuskanBot
# Merged version: original Muskan_Music _yt.py (same function names / signatures)
# + multi-source fallback downloader (API -> Worker API -> Shruti API -> yt-dlp -> JioSaavn -> SoundCloud)

import asyncio
import os
import re
import json
import glob
import random
import logging
from typing import Union
from urllib.parse import urlparse, quote

import aiohttp
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from py_yt import VideosSearch
try:
    from py_yt import Recommendations as _PyYtRec
except ImportError:
    _PyYtRec = None

import config
from config import LOGGER_ID, BASE_URL, API_KEY
from Muskan_Music import app
from Muskan_Music.helpers._store import is_on_off
from Muskan_Music.helpers._fmt import time_to_seconds

LOGGER = logging.getLogger(__name__)

STREAM_MODE = False

# Fallback APIs (third-party services - they can stop working any time).
# You can override them from Heroku Config Vars with these names.
WORKER_API_URL = os.getenv("WORKER_FALLBACK_API_URL", "https://youtubenewapi.skybotsdeveloper.workers.dev")
WORKER_API_KEY = os.getenv("WORKER_FALLBACK_API_KEY", "itsmesid")
SHRUTI_API_URL = os.getenv("SHRUTI_API_URL", "https://api.shrutibots.site")
SHRUTI_API_KEY = os.getenv("SHRUTI_API_KEY", "ShrutiBotsmz4lGsT87UWrai3SBsPK")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def safe_yt_shell(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False
        allowed = (
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
        )
        if not any(domain in p.netloc for domain in allowed):
            return False
        if any(x in url for x in [";", "|", "$", "`", "\n", "\r"]):
            return False
        return True
    except Exception:
        return False


def cookie_txt_file():
    cookie_dir = f"{os.getcwd()}/cookies"
    if os.path.exists(cookie_dir):
        files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
        if files:
            return os.path.join(cookie_dir, random.choice(files))
    if os.path.exists("cookies.txt"):
        return "cookies.txt"
    return None


def _cookie_args():
    ck = cookie_txt_file()
    return ["--cookies", ck] if ck else []


def _extract_id(link: str) -> str:
    if "youtu.be/" in link:
        return link.split("youtu.be/")[1].split("?")[0].split("&")[0]
    if "v=" in link:
        return link.split("v=")[-1].split("&")[0]
    return link.rstrip("/").split("/")[-1]


def _clean_title(title: str) -> str:
    t = re.sub(
        r"\(.*?\)|\[.*?\]|official|video|audio|lyrics?|lyrical",
        "",
        title or "",
        flags=re.IGNORECASE,
    )
    return re.sub(r"\s+", " ", t).strip()


def _ytdlp_base_opts() -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        # new yt-dlp needs a JS runtime for YouTube; Node is installed in the Docker image
        "js_runtimes": {"node": {}},
    }
    ck = cookie_txt_file()
    if ck:
        opts["cookiefile"] = ck
    return opts


def _ydl(opts: dict):
    try:
        return yt_dlp.YoutubeDL(opts)
    except Exception:
        opts = dict(opts)
        opts.pop("js_runtimes", None)
        return yt_dlp.YoutubeDL(opts)


def _pick_file(vid: str, final: str):
    if os.path.exists(final) and os.path.getsize(final) > 50000:
        return final
    for f in glob.glob(f"downloads/{vid}.*"):
        if f.endswith((".part", ".ytdl", ".json")):
            continue
        if os.path.getsize(f) > 50000:
            return f
    return None


async def _animated_progress(mystic, label: str, done_event: asyncio.Event):
    """No-op: progress shown only in inline button, not in caption."""
    await done_event.wait()


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ search / details helper â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

_TITLES = {}


async def _search_one(link: str):
    """Return dict(title, duration_min, duration_sec, thumb, vidid, link) or None.
    Tries py_yt first, then yt-dlp as a backup."""
    try:
        res = VideosSearch(link, limit=1)
        data = await asyncio.wait_for(res.next(), timeout=15)
        items = data.get("result") or []
        if items:
            it = items[0]
            dur = it.get("duration")
            if dur is None or str(dur) == "None":
                dur_sec = 0
            else:
                dur_sec = int(time_to_seconds(dur))
            return {
                "title": it["title"],
                "duration_min": dur,
                "duration_sec": dur_sec,
                "thumb": it["thumbnails"][0]["url"].split("?")[0],
                "vidid": it["id"],
                "link": it.get("link") or f"https://www.youtube.com/watch?v={it['id']}",
            }
    except Exception as e:
        LOGGER.warning(f"py_yt search failed: {e}")

    try:
        opts = _ytdlp_base_opts()
        opts["extract_flat"] = True
        q = link if re.search(r"youtube\.com|youtu\.be", link) else f"ytsearch1:{link}"
        loop = asyncio.get_running_loop()
        r = await loop.run_in_executor(
            None, lambda: _ydl(opts).extract_info(q, download=False)
        )
        e = r["entries"][0] if r and r.get("entries") else r
        if e and e.get("id"):
            sec = int(float(e.get("duration") or 0))
            m, s = divmod(sec, 60)
            h, m = divmod(m, 60)
            dur = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
            vid = e["id"]
            return {
                "title": e.get("title") or "Unknown",
                "duration_min": dur,
                "duration_sec": sec,
                "thumb": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
                "vidid": vid,
                "link": f"https://www.youtube.com/watch?v={vid}",
            }
    except Exception as e:
        LOGGER.error(f"yt-dlp search fallback failed: {e}")
    return None


async def _title_for(vid: str):
    if vid in _TITLES:
        return _TITLES[vid]
    info = await _search_one(f"https://www.youtube.com/watch?v={vid}")
    _TITLES[vid] = info["title"] if info else None
    return _TITLES[vid]


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ download sources â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _save_url(session, url: str, path: str, params=None):
    async with session.get(url, params=params) as r:
        if r.status not in (200, 206):
            return None
        if "text/html" in (r.headers.get("Content-Type") or "").lower():
            return None
        with open(path, "wb") as f:
            async for c in r.content.iter_chunked(131072):
                f.write(c)
    if os.path.exists(path) and os.path.getsize(path) > 50000:
        return path
    try:
        os.remove(path)
    except Exception:
        pass
    return None


async def _primary_api(vid: str, kind: str, wait: int):
    """Original BASE_URL / API_KEY flow (now it never raises on HTML replies)."""
    if not BASE_URL or not API_KEY:
        return None
    ext = "mp3" if kind == "song" else "mp4"
    p = f"downloads/{vid}.{ext}"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as s:
            url = (
                f"{BASE_URL}/api/{kind}?query={vid}&api={API_KEY}"
                if STREAM_MODE
                else f"{BASE_URL}/api/{kind}?query={vid}&download=true&api={API_KEY}"
            )
            async with s.get(url) as r:
                j = await r.json(content_type=None)
            u = j.get("stream")
            if not u:
                return None
            if j.get("type") == "live":
                return u
            for _ in range(wait):
                async with s.get(u) as r:
                    if r.status in (200, 206):
                        break
                    if r.status in (204, 423, 404, 410):
                        await asyncio.sleep(2)
                        continue
                    return None
            else:
                return None
            if STREAM_MODE:
                return u
            return await _save_url(s, u, p)
    except Exception as e:
        LOGGER.warning(f"primary API failed: {e}")
        return None


async def _dl_api(base: str, key: str, vid: str, kind: str):
    if not base or not key:
        return None
    ext = "mp3" if kind == "song" else "mp4"
    p = f"downloads/{vid}.{ext}"
    try:
        t = aiohttp.ClientTimeout(total=300, sock_connect=8, sock_read=20)
        async with aiohttp.ClientSession(timeout=t) as s:
            return await _save_url(
                s,
                f"{base}/download",
                p,
                params={
                    "url": vid,
                    "type": "audio" if kind == "song" else "video",
                    "api_key": key,
                },
            )
    except Exception as e:
        LOGGER.warning(f"fallback API {base} failed: {e}")
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass
        return None


async def _ytdlp_download(link: str, vid: str, kind: str):
    ext = "mp3" if kind == "song" else "mp4"
    final = f"downloads/{vid}.{ext}"
    opts = _ytdlp_base_opts()
    opts["outtmpl"] = f"downloads/{vid}.%(ext)s"
    if kind == "song":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        opts["format"] = "bestvideo[height<=?720]+bestaudio/best[height<=?720]/best"
        opts["merge_output_format"] = "mp4"
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: _ydl(opts).download([link]))
    return _pick_file(vid, final)


async def _jiosaavn_download(vid: str):
    title = await _title_for(vid)
    if not title:
        return None
    q = quote(_clean_title(title))
    base = getattr(config, "JIOSAAVN_API", "https://saavn.dev/api/search/songs?query=")
    path = f"downloads/{vid}.mp3"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=90)) as s:
            async with s.get(f"{base}{q}") as r:
                if r.status != 200:
                    return None
                data = await r.json(content_type=None)
            results = ((data or {}).get("data") or {}).get("results") or []
            if not results:
                return None
            urls = results[0].get("downloadUrl") or []
            if not urls:
                return None
            return await _save_url(s, urls[-1]["url"], path)
    except Exception as e:
        LOGGER.warning(f"JioSaavn fallback failed: {e}")
        return None


async def _soundcloud_download(vid: str):
    title = await _title_for(vid)
    if not title:
        return None
    opts = _ytdlp_base_opts()
    opts.pop("cookiefile", None)
    opts["outtmpl"] = f"downloads/{vid}.%(ext)s"
    opts["format"] = "bestaudio/best"
    opts["postprocessors"] = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }]
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: _ydl(opts).download([f"scsearch1:{_clean_title(title)}"]),
        )
        return _pick_file(vid, f"downloads/{vid}.mp3")
    except Exception as e:
        LOGGER.warning(f"SoundCloud fallback failed: {e}")
        return None


async def _download_media(link: str, kind: str, exts: list[str], wait: int = 60, mystic=None):
    vid = _extract_id(link)
    os.makedirs("downloads", exist_ok=True)
    label = "â¬‡ï¸ á´…á´á´¡É´ÊŸá´á´€á´…ÉªÉ´É¢ sá´É´É¢..." if kind == "song" else "â¬‡ï¸ á´…á´á´¡É´ÊŸá´á´€á´…ÉªÉ´É¢ á´ Éªá´…á´‡á´..."

    done_event = asyncio.Event()
    progress_task = None
    if mystic:
        progress_task = asyncio.create_task(_animated_progress(mystic, label, done_event))

    async def _finish():
        done_event.set()
        if progress_task:
            try:
                await progress_task
            except Exception:
                pass

    try:
        if not STREAM_MODE:
            for e in exts:
                p = f"downloads/{vid}.{e}"
                if os.path.exists(p) and os.path.getsize(p) > 50000:
                    await _finish()
                    return p

        sources = [
            ("API", lambda: _primary_api(vid, kind, wait)),
            ("WORKER", lambda: _dl_api(WORKER_API_URL, WORKER_API_KEY, vid, kind)),
            ("SHRUTI", lambda: _dl_api(SHRUTI_API_URL, SHRUTI_API_KEY, vid, kind)),
            ("YTDLP", lambda: _ytdlp_download(link, vid, kind)),
        ]
        if kind == "song":
            sources += [
                ("JIOSAAVN", lambda: _jiosaavn_download(vid)),
                ("SOUNDCLOUD", lambda: _soundcloud_download(vid)),
            ]

        failed = []
        for name, fn in sources:
            try:
                res = await fn()
            except Exception as ex:
                LOGGER.warning(f"{name} failed for {vid}: {ex}")
                res = None
            if res:
                LOGGER.info(f"âœ… {kind} {vid} downloaded via {name}")
                await _finish()
                return res
            failed.append(name)
        raise Exception("all sources failed: " + ", ".join(failed))
    except Exception as e:
        await _finish()
        try:
            await app.send_message(
                LOGGER_ID,
                f"âŒ {kind.upper()} ERR\nðŸ”— `{link}`\nâš ï¸ `{str(e)[:100]}`",
            )
        except Exception:
            pass
        raise


async def download_song(link: str, mystic=None):
    return await _download_media(link, "song", ["mp3", "m4a", "webm"], 60, mystic=mystic)


async def download_video(link: str, mystic=None):
    return await _download_media(link, "video", ["mp4", "webm", "mkv"], 90, mystic=mystic)


async def check_file_size(link):
    if not safe_yt_shell(link):
        return None

    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            *_cookie_args(),
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f"Error:\n{stderr.decode()}")
            return None
        return json.loads(stdout.decode())

    def parse_size(formats):
        total_size = 0
        for format in formats:
            total_size += format.get("filesize") or 0
        return total_size

    info = await get_format_info(link)
    if info is None:
        return None

    formats = info.get("formats", [])
    if not formats:
        print("No formats found.")
        return None

    return parse_size(formats)


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ YouTubeAPI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        info = await _search_one(link)
        if not info:
            raise Exception("Failed to fetch track details")
        return (
            info["title"],
            info["duration_min"],
            info["duration_sec"],
            info["thumb"],
            info["vidid"],
        )

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        info = await _search_one(link)
        if not info:
            raise Exception("Failed to fetch title")
        return info["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        info = await _search_one(link)
        if not info:
            raise Exception("Failed to fetch duration")
        return info["duration_min"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        info = await _search_one(link)
        if not info:
            raise Exception("Failed to fetch thumbnail")
        return info["thumb"]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        if not safe_yt_shell(link):
            return 0, "Invalid or unsafe URL."
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
        except Exception as e:
            print(f"Video API failed: {e}")

        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            *_cookie_args(),
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]

        if not safe_yt_shell(link):
            return []

        args = ["yt-dlp", "-i", "--get-id", "--flat-playlist"]
        args.extend(_cookie_args())
        args.extend(["--playlist-end", str(limit), "--skip-download", link])

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        playlist_data = stdout.decode("utf-8")

        try:
            result = playlist_data.split("\n")
            result = [key for key in result if key.strip() != ""]
        except Exception:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        info = await _search_one(link)
        if not info:
            raise Exception("Failed to fetch track details")

        clean_title = info["title"].strip()
        if len(clean_title) > 14:
            clean_title = clean_title[:14].rstrip() + "...."

        track_details = {
            "title": clean_title,
            "link": info["link"],
            "vidid": info["vidid"],
            "duration_min": info["duration_min"],
            "thumb": info["thumb"],
        }
        return track_details, info["vidid"]

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        if not safe_yt_shell(link):
            return [], link

        ytdl_opts = {"quiet": True}
        ck = cookie_txt_file()
        if ck:
            ytdl_opts["cookiefile"] = ck
        ydl = _ydl(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except Exception:
                    continue
                if not "dash" in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except Exception:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                        }
                    )
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link

        if not safe_yt_shell(link):
            return None, None

        loop = asyncio.get_running_loop()

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            ck = cookie_txt_file()
            if ck:
                ydl_optssx["cookiefile"] = ck
            x = _ydl(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        if songvideo or songaudio:
            await download_song(link, mystic=mystic)
            vid_id = _extract_id(link)
            fpath = f"downloads/{vid_id}.mp3"
            return fpath
        elif video:
            try:
                downloaded_file = await download_video(link, mystic=mystic)
                if downloaded_file:
                    return downloaded_file, True
            except Exception as e:
                print(f"Video API failed: {e}")

            if await is_on_off(1):
                direct = True
                downloaded_file = await download_song(link, mystic=mystic)
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp",
                    *_cookie_args(),
                    "-g",
                    "-f",
                    "best[height<=?720][width<=?1280]",
                    link,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = False
                else:
                    file_size = await check_file_size(link)
                    if not file_size:
                        return None, None
                    total_size_mb = file_size / (1024 * 1024)
                    if total_size_mb > 250:
                        return None, None
                    direct = True
                    downloaded_file = await loop.run_in_executor(None, video_dl)
        else:
            direct = True
            downloaded_file = await download_song(link, mystic=mystic)
        return downloaded_file, direct

    # â”€â”€ AutoPlay â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    @staticmethod
    def _clean_ap_title(title: str) -> str:
        title = re.sub(r"\[[^\]]*\]|\([^\)]*\)", " ", title or "")
        title = re.sub(
            r"\b(official|video|audio|lyrics?|lyrical|remix|status|song|songs|"
            r"music|feat\.?|ft\.?|prod\.?|full|hd|4k|hq|visualizer|slowed|reverb)\b",
            " ",
            title,
            flags=re.IGNORECASE,
        )
        return re.sub(r"\s+", " ", title).strip()[:80]

    @staticmethod
    def _is_ok_result(item: dict, excluded: set, max_sec: int = 7200) -> bool:
        vid = item.get("id")
        dur = item.get("duration")
        title = item.get("title")
        if not vid or not dur or not title or vid in excluded:
            return False
        try:
            sec = int(time_to_seconds(str(dur)))
        except Exception:
            return False
        return 30 < sec <= max_sec

    async def autoplay(
        self,
        videoid: str,
        title: str = "",
        exclude_ids: set = None,
    ):
        """Return a related YouTube track dict for autoplay, or None."""
        excluded = set(exclude_ids) if exclude_ids else set()
        excluded.add(videoid)

        def _make_result(item: dict):
            vid = item.get("id")
            dur = item.get("duration")
            t = item.get("title", "")
            try:
                sec = int(time_to_seconds(str(dur)))
            except Exception:
                sec = 0
            views = (item.get("viewCount") or {}).get("short", "Unknown views")
            channel = (item.get("channel") or {}).get("name", "YouTube")
            return {
                "title": t,
                "duration_min": dur,
                "duration_sec": sec,
                "vidid": vid,
                "views": views,
                "channel": channel,
            }

        loop = asyncio.get_event_loop()

        # Strategy 1: YouTube native related (Recommendations)
        if _PyYtRec is not None:
            try:
                rec = _PyYtRec(videoid)
                data = await asyncio.wait_for(
                    loop.run_in_executor(None, rec.getNextResults), timeout=8.0
                )
                for item in (data.get("result") or []):
                    if self._is_ok_result(item, excluded):
                        return _make_result(item)
            except Exception:
                pass

        # Strategy 2: Title-based search fallback
        clean = self._clean_ap_title(title)
        query = f"{clean} song" if clean else "trending hindi songs"
        try:
            res = VideosSearch(query, limit=20)
            data = await asyncio.wait_for(res.next(), timeout=10.0)
            for item in (data.get("result") or []):
                if self._is_ok_result(item, excluded):
                    return _make_result(item)
        except Exception:
            pass

        return None
