import yt_dlp as youtube_dl
import discord
import os
import asyncio
from discord.ext import commands

# Insert path for video save
path = 'C:\\Users\\jadis\\Downloads\\my_reel.mp4'

# Function to download video from url using youtube_dl
def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': output_path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Define your intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.guilds = True  # Enable guilds intent
intents.messages = True # Enable message content

# Create a bot instance with a specified prefix for commands
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


# Define the download command 
@bot.command(name='download')
async def download(ctx, video_url: str):
    print(video_url)
    # Prompt the user for their preference
    question = await ctx.send("Do you want to receive the video in a channel or as a direct message? (Type `channel` or `dm`)")

    def check(response):
        return response.author == ctx.author and response.content.lower() in ['channel', 'dm']

    try:
        user_response = await bot.wait_for('message', check=check, timeout=30)
        preference = user_response.content.lower()

        # Download the video 
        download_video(video_url, path)

        if preference == 'channel':
            # Send the video to the same channel where the user typed the command
            await ctx.channel.send(file=discord.File(path))

        elif preference == 'dm':
            # Send the video as a direct message to the user
            await ctx.author.send(file=discord.File(path))

        # Delete the video from the output path
        os.remove(path)

        # Delete the user's command from the channel
        await ctx.message.delete()
        # Delete the user's response
        await user_response.delete()
        # Delete bots question 
        await question.delete()

    except asyncio.TimeoutError:
        await ctx.channel.send("You took too long to respond. Please try again.")


# Run the bot
bot.run('MTIxODcxMzY0NDY0MTE2MTI4Ng.GwaHFL.WXPrRNe47qo_bPaaclRMD4t_-fVhOecJlvZeD0')

