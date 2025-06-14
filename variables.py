'''Edit variables here to change bot.py settings'''
from collections import deque
import shelve
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()

'''Python variables'''
# Decide how many seconds needed to trigger outro
outro_trigger = 11 # Set to 11 seconds for testing purposes. Change to desired value in seconds.

# Add path for audio files to save at
Path = "audio\\"

# Add owner user id here to run owner specific commands
Owner = int(os.getenv("OWNER"))

# Queue to manage audio playback order
audio_queue = deque(maxlen=3)  # Set the queue limit to 3

# Load existing data from dict that maps user IDs to audio file paths
# Can be altered via request command
def load_audio_files():
    """Load audio files from database, ensuring fresh data"""
    with shelve.open('audio_paths') as db:
        return dict(db.get('user_audio_paths', {}))

# Initial load of audio files
user_audio_files = load_audio_files()

# Path to ffmpeg.exe
ffmpeg_path = "C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe"

bot_token = os.getenv("TOKEN")

'''Discord variables'''
# Intitialize bot and tree
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), 
                   intents=discord.Intents.all())  # commands.when_mentioned_or("!") is used to make the bot respond to !ping and @bot ping
tree= bot.tree

'''OPTIONAL'''
# Add server ids you would like to target for your commands 
# You will need to uncomment the guilds line in the command decorators located in disc_functions
#servers=[
#    discord.Object(id="server id in integer format"), # Personal Server
#    discord.Object(id="server id in integer format") # Friends Server
#]

servers=[
    discord.Object(id=int(os.getenv("PRSSERVER"))), # Personal Server
    discord.Object(id=int(os.getenv("FRSERVER"))) # Friends Server
]

server = discord.Object(id=int(os.getenv("PRSSERVER")))

