import discord
from discord import app_commands
import yt_dlp as youtube_dl
import os
import asyncio
import enum

# Insert path for video save
path = 'C:\\Users\\jadis\\Downloads\\my_video.mp4'

# Function to download video from url using youtube_dl
def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': output_path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Define your intents (including the necessary ones)
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.guilds = True  # Enable guilds intent

# Initialize your Discord bot client with the intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Wake up Bot
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    await tree.sync(guild=discord.Object(id=1203407209397231686)) # Run for auto sync everytime bot boots up

# Create choices to user 
class Share(str, enum.Enum):
    yes = "yes"
    no= "no"

# Define the download command 
@tree.command(
    name="download",
    description="Download videos from links",
    guild=discord.Object(id=1203407209397231686) # Add this to specify server for command
)
# Provide instructions to user
@app_commands.describe(video_url = "Type your url", share = "Would you like to share this video with the channel?")

# Create download function
async def download(interaction: discord.Interaction, video_url: str, share: Share):

    try:
        # Download the video 
        download_video(video_url, path)

        # If user choice is to share to channel
        if share.lower() == "yes":
            # Send the video to the same channel where the user interacted with the bot
            await interaction.response.send_message(file = discord.File(path))

        # If user choice is not to share to channel
        elif share.lower() == "no":
            # Send the video to the same channel but user can only view
            await interaction.response.send_message(file = discord.File(path), ephemeral= True)

        # Delete the video from the output path
        os.remove(path)

    except asyncio.TimeoutError:
        await interaction.response.send_message("You took too long to respond. Please try again.")

# Define the sync command 
@tree.command(
    name="sync",
    description="Owner only",
    guild=discord.Object(id=1203407209397231686)
)

# Owner only command to sync command trees in all servers that bot is deployed in
async def sync(interaction):
    if interaction.user.id == 426031900633858048:
        await tree.sync()
        await interaction.response.send_message('Command tree synced.', ephemeral = True)
    else:
        await interaction.response.send_message('You must be the owner to use this command!', ephemeral = True)

client.run("MTIxODcxMzY0NDY0MTE2MTI4Ng.GwaHFL.WXPrRNe47qo_bPaaclRMD4t_-fVhOecJlvZeD0")