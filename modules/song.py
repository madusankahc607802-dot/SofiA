import yt_dlp
import os
from datetime import datetime
from config import COOKIE_FILE
import re
import tempfile

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_song(query):
    # Temporary file
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    filepath = tmpfile.name
    tmpfile.close()

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "ffmpeg_location": "/app/vendor/ffmpeg/bin",  # ✅ Correct Heroku ffmpeg path
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
        "outtmpl": filepath
    }

    if COOKIE_FILE:
        ydl_opts["cookiefile"] = COOKIE_FILE

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch:{query}", download=True)
            
            if "entries" not in search_result or len(search_result["entries"]) == 0:
                raise ValueError(f"No results found for: {query}")

            info = search_result["entries"][0]

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
