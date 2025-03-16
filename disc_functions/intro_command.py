import asyncio
import concurrent.futures
import discord
from discord import app_commands
import os
from py_functions.download_audio import download_audio
from py_functions.totalseconds import totalseconds
from py_functions.sync_db import sync_db
from variables import Path, user_audio_files, tree # Change from variables to configs to run on your own bot

async def download_and_store_audio(video_url: str, start: int, end: int, user_id: str):
    '''download users intro audio and store in user_audio_files dictionary'''
    loop = asyncio.get_running_loop()
    try:
        if end - start > 10: # If audio is longer than 10 seconds
            end = start + 10 # Set end to 10 seconds

        with concurrent.futures.ThreadPoolExecutor() as pool:
            audio_title = await loop.run_in_executor(pool, download_audio, video_url, Path, start, end) # Download audio
        audio_path = f'{Path}{audio_title}.mp3' # Create audio path

        if user_id in user_audio_files: # Check if user exists
            if user_audio_files[user_id][0]: # Check if user already has intro
                os.remove(user_audio_files[user_id][0]) # Delete old intro
            user_audio_files[user_id][0] = audio_path # Store new intro

        sync_db() # Update database

        return audio_path # Return new audio path
    except Exception as e:
        return str(e)

@tree.command(
    name="intro",
    description="Tell me what intro song you would like",
    #guilds=servers
)
@app_commands.describe(video_url="Type your url", start="Where do you want to start the download?", end="Where do you want to end the download?")
async def intro(interaction: discord.Interaction, video_url: str, start: str, end: str):
    ''' intro function for users to change intro audio triggered by the /intro command'''
    start = totalseconds(start) # Convert timestamps to only seconds
    end = totalseconds(end) # Convert timestamps to only seconds
    user_id = str(interaction.user.id) # Get user ID

    if user_id not in user_audio_files: # If user not in keys then add them
        user_audio_files[user_id] = [None, None] 

    await interaction.response.defer(ephemeral=True) # Defer response

    audio_path = await download_and_store_audio(video_url, start, end, user_id) # Download and store audio path

    if os.path.exists(audio_path): # Check if audio path leads to a file
        await interaction.edit_original_response(content="Your intro has been added")
    else:
        await interaction.edit_original_response(content=f"Error:{audio_path}")
