'''Edit variables here to change bot.py settings'''
from collections import deque
import shelve
from discord import app_commands
import discord

# Add path for audio files to save at
Path = "audio\\" # Add \\ at the end of your path

# Add owner user id here to run owner specific commands
Owner = "add user id here in integer format"

# Queue to manage audio playback order
audio_queue = deque(maxlen=3)  # Change maxlen to increase or decrease queue limit

# Initialize the shelve database
audio_db = shelve.open('audio_paths.db', writeback=True)

# Load existing data (if any) from dict that maps user IDs to audio file paths
# Can be altered via request command
user_audio_files = audio_db.get('user_audio_paths', {})

# Path to ffmpeg.exe
ffmpeg_path = "C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe"

# Input your token to run bot
client_token = "input token here"

'''Discord variables'''
# Initialize the bot with intents (required for certain events)
intents = discord.Intents.default()
intents.voice_states = True  # Enable voice state events
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Add server ids you would like to target for your commands 
'''OPTIONAL'''
#servers=[
#    discord.Object(id="server id in integer format"), # Personal Server
#    discord.Object(id="server id in integer format") # Friends Server
#]
