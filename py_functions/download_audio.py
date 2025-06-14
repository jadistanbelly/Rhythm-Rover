import yt_dlp
from yt_dlp.utils import download_range_func
import time
import os
from .hash_utils import create_stable_hash, update_hash_lookup

def download_audio(url, output_path, start, end, max_retries=3):
    """Download audio from url using yt-dlp with retry logic"""
    # Split youtube video from playlist
    url = url.split("&list=")[0] if "&list=" in url else url

    # Enhanced options for more reliable downloads
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 10,
        'force_keyframes_at_cuts': True,
        'quiet': False
    }

    # First get video info
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            # Create hash-based title
            title_hash = create_stable_hash(info_dict['title'])
            video_title = f'audio_{title_hash}_{start}_{end}'
            
            # Ensure the output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Update the hash lookup file with video metadata
            update_hash_lookup(title_hash, info_dict['title'], url, output_path)
    except Exception as e:
        raise Exception(f"Failed to get video info: {str(e)}")

    # Add download specific options
    ydl_opts.update({
        'outtmpl': os.path.join(output_path, f'{video_title}.%(ext)s'),
        'download_ranges': download_range_func(None, [(start,end)]),
    })

    # Attempt download with retries
    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return video_title
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise Exception(f"Failed to download after {max_retries} attempts: {str(e)}")
            print(f"Download attempt {attempt + 1} failed, retrying...")
            time.sleep(2)  # Wait 2 seconds before retrying

    return video_title