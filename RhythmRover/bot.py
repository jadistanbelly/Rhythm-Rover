import discord
import asyncio
from collections import deque
from discord import app_commands
import yt_dlp
from yt_dlp.utils import download_range_func
import shelve

# Add path for audio files to save at 
path = "audio\\"

# Add owner user id here to run owner specific commands
owner = 426031900633858048

# Function to download audio from url using youtube_dl
def download_audio(url, output_path, start, end):
    ydl_opts = {
        'extract_audio': True,
        'format': 'bestaudio',
        'outtmpl': f'{output_path}''%(title)s.mp3', # Title audio file as per video title from url
        'download_ranges': download_range_func(None, [(start, end)]), # Specified timestamps in int format
        'force_keyframes_at_cuts': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download = True)
        video_title = info_dict['title']
        print(video_title)
        ydl.download([url])
    return video_title

# Initialize the bot with intents (required for certain events)
intents = discord.Intents.default()
intents.voice_states = True  # Enable voice state events
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Initialize the shelve database
audio_db = shelve.open('audio_paths.db', writeback=True)

# Load existing data (if any) from dict that maps user IDs to audio file paths
# Can be altered via request command
user_audio_files = audio_db.get('user_audio_paths', {})

# Queue to manage audio playback order
audio_queue = deque(maxlen=3)  # Set the queue limit to 3

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} ({client.user.id})")
    await tree.sync(guild=discord.Object(id=169178811429027840)) # Run for auto sync everytime bot boots up

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel:  # User joined a voice channel
            user_id = str(member.id)
            if user_id in user_audio_files:
                print(user_audio_files)
                audio_file_path = user_audio_files[user_id]
                print(user_id)
                print(audio_file_path)
                audio_queue.append(audio_file_path)  # Add to the queue

                # If the queue is not empty and the bot is not currently playing
                if audio_queue and not client.voice_clients:
                    await play_next_audio(after.channel)

async def play_next_audio(channel):
    while audio_queue:
        audio_file_path = audio_queue.popleft()
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe", source=audio_file_path))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

# Define the download command 
@tree.command(
    name="request",
    description="Tell me what intro song you would like",
    guilds=[
        discord.Object(id=1203407209397231686), # Personal Server
        discord.Object(id=169178811429027840) # Og Crue Server
    ]
)
# Provide instructions to user
@app_commands.describe(video_url = "Type your url", start = "Where do you want to start the download?", end = "Where do you want to end the download?")

# Create request function
async def request(interaction: discord.Interaction, video_url: str, start: int, end: int):

    try:
        if end-start <= 10: 

            # Open shelve if closed
            audio_db.open()

            # Download the video 
            audio_title = download_audio(video_url, path, start, end)

            # Insert User ID and path of downloaded audio file
            user_audio_files[str(interaction.user.id)] = f'{path}{audio_title}.mp3'

            # Update Shelf DB 
            audio_db['user_audio_paths'] = user_audio_files

            # Save changes immediately
            audio_db.sync()  

            # Close the shelve database when done
            audio_db.close()

            # Respond back to user
            await interaction.response.send_message("Your intro has been added", ephemeral = True)

        else:
            # Open shelve if closed
            audio_db.open()
            
            # Download the video 
            audio_title = download_audio(video_url, path, start, start+10)

            # Insert User ID and path of downloaded audio file
            user_audio_files[str(interaction.user.id)] = f'{path}{audio_title}.mp3'

            # Update Shelf DB 
            audio_db['user_audio_paths'] = user_audio_files

            # Save changes immediately
            audio_db.sync()  

            # Close the shelve database when done
            audio_db.close()

            # Respond back to user
            await interaction.response.send_message("Your intro has been added", ephemeral = True)
    except asyncio.TimeoutError:
        await interaction.response.send_message("You took too long to respond. Please try again.", ephemeral = True)


# Define the sync command 
@tree.command(
    name="sync",
    description="Owner only",
    guilds=[
        discord.Object(id=1203407209397231686), # Personal Server
        discord.Object(id=169178811429027840) # Og Crue Server
    ]
)

# Owner only command to sync command trees in all servers that bot is deployed in
async def sync(interaction):
    if interaction.user.id == owner: 
        await tree.sync()
        await interaction.response.send_message('Command tree synced.', ephemeral = True)
    else:
        await interaction.response.send_message('You must be the owner to use this command!', ephemeral = True)


# Run the bot
client.run("MTIyMTUzMDcyMTQ5MjAwOTA2MQ.GHwATW.4LerKAQ041vJ6XxDpzMFBrwrPgtVm86Sao-RN4")

