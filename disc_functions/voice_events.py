import discord
import asyncio
from variables import audio_queue, ffmpeg_path, bot, user_audio_files, outro_trigger # Change from variables to configs to run on your own bot
from datetime import datetime

# Store user join times to determine when to play outro
user_join_times = {}

async def handle_voice_state_update(member, before, after):
    '''track if user joins voice channel'''
    user_id = str(member.id)
    try:
        if before.channel != after.channel: # User joined or left a voice channel
            if after.channel:  # User joined a voice channel
                user_join_times[user_id] = datetime.now() # Store the time user joined
                if user_id in user_audio_files: # Check if user exists
                    audio_file_path = user_audio_files[user_id][0] # Get intro path
                    audio_queue.append(audio_file_path)  # Add to the queue
                    if audio_queue and not bot.voice_clients and len(audio_queue) > 0: # If the queue is not empty and the bot is not currently playing
                        await play_next_audio(after.channel) # Play intro

                '''play audio when user leaves voice channel'''
            else: # User left a voice channel
                if user_id in user_audio_files: # Check if user exists
                    join_time = user_join_times[user_id] # Get user join time
                    leave_time = datetime.now() # Get user leave time
                    difference = (leave_time - join_time).seconds # Calculate difference in seconds
                    if difference > outro_trigger: # Change outro_trigger to determine when to play outro in configs.py
                            audio_file_path = user_audio_files[user_id][1] # Get outro path
                            audio_queue.append(audio_file_path)  # Add to the queue
                            if not bot.voice_clients: # If the bot is not currently playing
                                await play_next_audio(before.channel) # Play outro
    except (TypeError, IndexError, KeyError): # Disconnect bot from Voice Channel if user is missing intro/outro
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        await voice_client.disconnect()

async def play_next_audio(channel):
    '''play audio in queue'''
    while audio_queue: # While the queue is not empty
        audio_file_path = audio_queue.popleft() # Get the first item in the queue
        try:
            vc = await channel.connect() # Connect to voice channel
        except discord.ClientException: # If the bot is already in a voice channel
            vc = channel.guild.voice_client # Get the voice client
        await asyncio.sleep(0.5) # Wait 0.5 second before playing for bot to join channel
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=audio_file_path)) # Play audio
        print(f'Currently Playing: {audio_file_path}',
              f'Queue total: {len(audio_queue)}') # Show what is playing and queue length
        while vc.is_playing(): # Check if audio is playing
            await asyncio.sleep(1) # Wait for audio to finish
        await vc.disconnect() # Disconnect
