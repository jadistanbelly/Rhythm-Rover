'''Import required modules'''
import discord
from disc_functions.intro_command import intro
from disc_functions.outro_command import outro
from disc_functions.sync_command import sync
from disc_functions.kill_command import kill
from disc_functions.voice_events import on_voice_state_update, play_next_audio
from disc_functions.delete_command import delete
from variables import bot, bot_token # Change from variables to configs to run on your own bot

# Identify bot login information
@bot.event
async def on_ready():
    print("Logged in as:",
          f"{bot.user.name} ({bot.user.id})")
    
# Call intro function to bot.py
async def call_intro(interaction: discord.Interaction, video_url: str, start: str, end: str):
    await intro(interaction, video_url, start, end)

# Call outro function to bot.py
async def call_outro(interaction: discord.Interaction, video_url: str, start: str, end: str):
    await outro(interaction, video_url, start, end)

# Call sync function to bot.py
async def call_sync(interaction):
    await sync(interaction)

# Call kill function to bot.py
async def call_kill(interaction):
    await kill(interaction)

# Call delete function to bot.py
async def call_delete(interaction: discord.Interaction, choice: str):
    await delete(interaction, choice)

# Call on_voice_state_update function to bot.py
async def call_on_voice_state_update(member, before, after):
    await on_voice_state_update(member, before, after)

# Call play_next_audio function to bot.py
async def call_play_next_audio(channel):
    await play_next_audio(channel)

# Run the bot
bot.run(bot_token)
