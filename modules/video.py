import yt_dlp
import os
from datetime import datetime
from config import COOKIE_FILE
import re
import tempfile

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_video(query):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
    }

    if COOKIE_FILE:
        ydl_opts["cookiefile"] = COOKIE_FILE

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    filepath = tmpfile.name
    tmpfile.close()

    ydl_opts["outtmpl"] = filepath

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)["entries"][0]

        upload_date = info.get("upload_date")
        upload_date_str = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}" if upload_date else "N/A"

        data = {
            "title": info.get("title"),
            "channel": info.get("uploader") or "Unknown",
            "category": info.get("categories", ["N/A"])[0] if info.get("categories") else "N/A",
            "upload_date": upload_date_str,
            "upload_time": upload_date or "N/A",
            "duration": str(datetime.utcfromtimestamp(info.get("duration", 0)).strftime("%H:%M:%S")),
            "views": info.get("view_count"),
            "likes": info.get("like_count"),
            "dislikes": info.get("dislike_count", "N/A"),
            "comments": info.get("comment_count"),
            "thumbnail": info.get("thumbnail"),
            "url": info.get("webpage_url"),
            "id": info.get("id"),
            "uploader": info.get("uploader") or "Unknown",
            "file_size": info.get("filesize_approx") or 0,
            "license": info.get("license", "N/A"),
            "age_restricted": "Yes" if info.get("age_limit", 0) > 0 else "No",
            "filepath": filepath
        }

        return filepath, data

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        raise e
