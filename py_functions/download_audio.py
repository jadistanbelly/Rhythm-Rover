import yt_dlp
from yt_dlp.utils import download_range_func
import subprocess
import re
import os

# Function to download audio from url using yt_dlp
def download_audio(url, output_path, start, end):

    # Split video link from playlist
    if "&list=" in url:
        split = url.split("&list=")
        url = split[0]

    # Get title of download 
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False) # dont download url yet
        base_title = info_dict['title'] # Extract title 
        clean_title = re.sub(r'[^\w\s]', '', base_title) # Clean title of any special characters 
        print(clean_title)
        video_title = f'{clean_title}{str(start)}{str(end)}' # create unique title name
        print(video_title)

    # Setup options for ydl
    ydl_opts = {
        'extract_audio': True,
        'format': 'bestaudio',
        'outtmpl': f'{output_path}{video_title}.mp3', # Title audio file as per video title from url including timestamps
        'download_ranges': download_range_func(None, [(start,end)]), # Specified timestamps in int format
        'force_keyframes_at_cuts': True,
        #'noplaylist': True # Code not working
    }
    try: # Try just audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return video_title
        
    except: # fallback to video format
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
        ydl_opts['outtmpl'] = f'{output_path}{video_title}.mp4'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

            # Convert to audio
            subprocess.run(["ffmpeg", "-i", f'{output_path}{video_title}.mp4', "-vn", "-acodec", "libmp3lame", "-y", f'{output_path}{video_title}.mp3'])

            # Delete Video
            os.remove(f'{output_path}{video_title}.mp4')

            # Return audio title
            return video_title
