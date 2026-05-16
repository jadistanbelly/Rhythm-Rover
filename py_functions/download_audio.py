import os
import time

import yt_dlp
from yt_dlp.utils import download_range_func

from .hash_utils import create_stable_hash, update_hash_lookup


def download_audio(url, output_path, start, end, max_retries=3):
    """Download audio from url using yt-dlp with retry logic"""
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "socket_timeout": 30,
        "retries": 10,
        "fragment_retries": 10,
        "force_keyframes_at_cuts": True,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get("title") or "audio"
            title_hash = create_stable_hash(title)
            video_title = f"audio_{title_hash}_{start}_{end}"
            
            os.makedirs(output_path, exist_ok=True)
            
            update_hash_lookup(title_hash, title, url, output_path)
    except Exception as exc:
        raise RuntimeError("Failed to get video info") from exc

    ydl_opts.update({
        "outtmpl": os.path.join(output_path, f"{video_title}.%(ext)s"),
        "download_ranges": download_range_func(None, [(start, end)]),
    })

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return video_title
        except Exception as exc:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to download after {max_retries} attempts") from exc
            print(f"Download attempt {attempt + 1} failed, retrying...")
            time.sleep(2)

    return video_title
