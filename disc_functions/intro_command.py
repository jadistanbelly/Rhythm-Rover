import asyncio
import logging
from pathlib import Path as FilePath

import discord
from discord import app_commands

from py_functions.audio_files import safe_remove_audio_file
from py_functions.download_audio import download_audio
from py_functions.sync_db import sync_db
from py_functions.validation import normalize_clip_request
from variables import Path, tree, user_audio_files

logger = logging.getLogger(__name__)


async def download_and_store_audio(video_url: str, start: str, end: str, user_id: str):
    """Download a user's intro audio and store it in user_audio_files."""
    try:
        video_url, start_seconds, end_seconds = normalize_clip_request(video_url, start, end)
        audio_title = await asyncio.to_thread(
            download_audio,
            video_url,
            Path,
            start_seconds,
            end_seconds,
        )
        audio_path = str(FilePath(Path) / f"{audio_title}.mp3")

        user_audio_files.setdefault(user_id, [None, None])
        safe_remove_audio_file(user_audio_files[user_id][0], Path)
        user_audio_files[user_id][0] = audio_path

        sync_db()
        return audio_path
    except ValueError as exc:
        return str(exc)
    except Exception:
        logger.exception("Failed to store intro audio")
        return "Failed to download intro audio. Check the URL and timestamps, then try again."


@tree.command(
    name="intro",
    description="Tell me what intro song you would like",
    #guilds=servers
)
@app_commands.describe(video_url="Type your url", start="Where do you want to start the download?", end="Where do you want to end the download?")
async def intro(interaction: discord.Interaction, video_url: str, start: str, end: str):
    """Register intro audio for the current user."""
    user_id = str(interaction.user.id)

    await interaction.response.defer(ephemeral=True)

    audio_path = await download_and_store_audio(video_url, start, end, user_id)

    if FilePath(audio_path).exists():
        await interaction.edit_original_response(content="Your intro has been added")
    else:
        await interaction.edit_original_response(content=f"Error:{audio_path}")
