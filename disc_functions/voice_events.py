import discord
import asyncio
from variables import audio_queue, ffmpeg_path, bot, user_audio_files, outro_trigger # Change from variables to configs to run on your own bot
from datetime import datetime

# Store user join times to determine when to play outro
user_join_times = {}
@bot.event
async def on_voice_state_update(member, before, after):
    '''track if user joins voice channel'''
    if before.channel != after.channel:
        if after.channel:  # User joined a voice channel
            user_id = str(member.id)
            #print(f'User Joined Voice Channel: {user_id}')
            user_join_times[user_id] = datetime.now() # Store the time user joined
            if user_id in user_audio_files:
                #print(f'User Dictionary: {user_audio_files}')
                audio_file_path = user_audio_files[user_id][0] # Get intro path
                #print(f'Audio File Path: {audio_file_path}')
                audio_queue.append(audio_file_path)  # Add to the queue
                #print(f'Audio Queue: {audio_queue}')
                # If the queue is not empty and the bot is not currently playing
                if audio_queue and not bot.voice_clients:
                    await play_next_audio(after.channel)

            '''play audio when user leaves voice channel'''
        else: # User left a voice channel
            user_id = str(member.id)
            if user_id in user_audio_files:
                join_time = user_join_times[user_id]
                leave_time = datetime.now()
                difference = (leave_time - join_time).seconds
                if difference > outro_trigger: # Change outro_trigger to determine when to play outro in configs.py
                    try: 
                        audio_file_path = user_audio_files[user_id][1] # Get outro path
                        audio_queue.append(audio_file_path)  # Add to the queue
                        await play_next_audio(before.channel) # Play outro
                    except IndexError:
                        print("Outro not setup for user")

                else:
                    print('User left voice channel too soon to trigger outro')

async def play_next_audio(channel):
    '''play audio in queue'''
    while audio_queue:
        audio_file_path = audio_queue.popleft()
        vc = await channel.connect()
        await asyncio.sleep(0.5) # Wait 0.5 second before playing for bot to join channel
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=audio_file_path))
        print(f'Currently Playing: {audio_file_path}',
              f'Queue total: {len(audio_queue)}') # Show what is playing and queue length
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
