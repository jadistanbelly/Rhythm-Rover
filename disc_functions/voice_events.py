import asyncio
from datetime import datetime
from pathlib import Path as FilePath

import discord

from variables import audio_queue, bot, ffmpeg_path, outro_trigger, user_audio_files

# Store user join times to determine when to play outro
user_join_times = {}

async def handle_voice_state_update(member, before, after):
    """Track voice-channel joins and leaves for intro/outro playback."""
    user_id = str(member.id)
    try:
        if before.channel == after.channel:
            return

        if after.channel:
            user_join_times[user_id] = datetime.now()
            audio_file_path = user_audio_files.get(user_id, [None, None])[0]
            if audio_file_path:
                audio_queue.append(audio_file_path)
                if not bot.voice_clients:
                    await play_next_audio(after.channel)
            return

        join_time = user_join_times.pop(user_id, None)
        audio_file_path = user_audio_files.get(user_id, [None, None])[1]
        if join_time is None or not audio_file_path:
            return

        difference = (datetime.now() - join_time).seconds
        if difference > outro_trigger:
            audio_queue.append(audio_file_path)
            if not bot.voice_clients:
                await play_next_audio(before.channel)
    except (TypeError, IndexError, KeyError):
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client:
            await voice_client.disconnect()

async def play_next_audio(channel):
    """Play audio in queue."""
    while audio_queue:
        audio_file_path = audio_queue.popleft()
        if not audio_file_path or not FilePath(audio_file_path).exists():
            continue

        try:
            vc = await channel.connect()
        except discord.ClientException:
            vc = channel.guild.voice_client

        await asyncio.sleep(0.5)
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=audio_file_path))
        print(f"Currently Playing: {audio_file_path}", f"Queue total: {len(audio_queue)}")
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
