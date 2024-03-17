import yt_dlp as youtube_dl
import discord
import os

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


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

@client.event
async def on_message(message):
    if message.content.startswith('/download'):
        try:
            # Extract the video URL from the message
            video_url = message.content.split(' ')[1]

            # Download the video
            download_video(video_url, 'C:\\Users\\jadis\\Downloads\\my_reel.mp4')

            # Send the video to a specified channel
            channel_id = 1203407324681863208  # Replace with your channel ID
            channel = client.get_channel(channel_id)
            await channel.send(file=discord.File('C:\\Users\\jadis\\Downloads\\my_reel.mp4'))

            # Delete the video from the output path
            os.remove('C:\\Users\\jadis\\Downloads\\my_reel.mp4')

            # Delete the user's command from the channel
            await message.delete()

        except discord.errors.HTTPException as e:
            await channel.send(f"Failed to upload video, HTTP code: {e.status}")
            os.remove('C:\\Users\\jadis\\Downloads\\my_reel.mp4')

# Run the bot
client.run('MTIxODcxMzY0NDY0MTE2MTI4Ng.GwaHFL.WXPrRNe47qo_bPaaclRMD4t_-fVhOecJlvZeD0')


