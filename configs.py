'''Edit variables here to change bot.py settings'''
from collections import deque
import shelve
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
# Add path for audio files to save at
Path = "audio\\" # Add \\ at the end of your path

# Decide how many seconds needed to trigger outro
outro_trigger = 11 # Set to 11 seconds for testing purposes. Change to desired value in seconds.

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
bot_token = "input token here"
'''Or if using venv'''
#load_dotenv()
#bot_token = os.getenv("TOKEN")

'''Discord variables'''
# Intitialize bot and tree
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), 
                   intents=discord.Intents.all())  # commands.when_mentioned_or("!") is used to make the bot respond to !ping and @bot ping
tree= bot.tree

# Add server ids you would like to target for your commands 
'''OPTIONAL'''
#servers=[
#    discord.Object(id="server id in integer format"), # Personal Server
#    discord.Object(id="server id in integer format") # Friends Server
#]
