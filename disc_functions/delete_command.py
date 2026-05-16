import logging

import discord

from py_functions.audio_files import safe_remove_audio_file
from py_functions.sync_db import sync_db
from variables import Path, tree, user_audio_files

logger = logging.getLogger(__name__)


@tree.command(
    name="delete",
    description="Use only if you want to be permanently deleted",
    #guilds=servers
)
async def delete(interaction: discord.Interaction):
    """Delete the user's saved intro and outro audio."""
    try:
        user_id = str(interaction.user.id)
        intro_path, outro_path = user_audio_files[user_id]

        for audio_path in (intro_path, outro_path):
            try:
                safe_remove_audio_file(audio_path, Path)
            except ValueError:
                logger.warning("Skipped unsafe stored audio path for user %s", user_id)

        del user_audio_files[user_id]

        sync_db()
        await interaction.response.send_message("Deleted!", ephemeral=True)

    except KeyError:
        await interaction.response.send_message("You have no audio files to delete", ephemeral=True)
        
    except TypeError:
        if user_id in user_audio_files:
            del user_audio_files[user_id]
            sync_db()
            await interaction.response.send_message(
                "Partially deleted audio files and cleaned up data",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message("No data found to delete", ephemeral=True)
