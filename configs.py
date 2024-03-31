'''Edit variables here to change bot.py settings'''
from collections import deque
import discord

# Add path for audio files to save at
Path = "audio\\" # Add \\ at the end of your path

# Add owner user id here to run owner specific commands
Owner = "add user id here in integer format"

# Queue to manage audio playback order
audio_queue = deque(maxlen=3)  # Change maxlen to increase or decrease queue limit

# Path to ffmpeg.exe
ffmpeg_path = "C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe"

# Add server ids you would like to target in integer format OPTIONAL
servers=[
    discord.Object(id="server id in integer format"), # Personal Server
    discord.Object(id="server id in integer format") # Friends Server
]

# Input your token to run bot
client_token = "input token here"