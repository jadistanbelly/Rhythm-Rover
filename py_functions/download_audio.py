import yt_dlp
from yt_dlp.utils import download_range_func
import re

# Function to download audio from url using yt_dlp
def download_audio(url, output_path, start, end):
    # Split youtube video from playlist
    url = url.split("&list=")[0] if "&list=" in url else url

    with yt_dlp.YoutubeDL() as ydl: # Get title of download 
        info_dict = ydl.extract_info(url, download=False) # False, so we can extract title first
        clean_title = re.sub(r'[^\w\s]', '_', info_dict['title']) # Extract and clean title of any special characters 
        video_title = f'{clean_title}_{str(start)}_{str(end)}' # create unique title name

    # Setup options for ydl
    ydl_opts = {
        'outtmpl': f'{output_path}{video_title}.%(ext)s', # Title audio file as per video title from url including timestamps
        'download_ranges': download_range_func(None, [(start,end)]), # Specified timestamps in int format
        'force_keyframes_at_cuts': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}], # Use FFMPEG to extract audio from video
        'quiet': True} # Remove quiet if you would like to see the progress of the download in console

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url]) # Download audio from url         
        
    return video_title
