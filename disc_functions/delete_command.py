from variables import tree, user_audio_files
import discord
import os
from py_functions.sync_db import sync_db

@tree.command(
    name="delete",
    description="Use only if you want to be permanently deleted",
    #guilds=servers
)
async def delete(interaction: discord.Interaction):
    '''Command to delete user intro and/or outro'''
    try:
        user_id = str(interaction.user.id)
        intro_path, outro_path = user_audio_files[user_id]

        if os.path.exists(intro_path): os.remove(intro_path)
        if os.path.exists(outro_path): os.remove(outro_path)
        del user_audio_files[user_id]

        sync_db()
        await interaction.response.send_message(f'Deleted!', ephemeral=True)

    except KeyError:
        await interaction.response.send_message(f'You have no audio files to delete', ephemeral=True)
        
    except (TypeError, FileNotFoundError):
        if user_id in user_audio_files:
            del user_audio_files[user_id]
            sync_db()
            await interaction.response.send_message(f'Partially deleted audio files and cleaned up data', ephemeral=True)
        else:
            await interaction.response.send_message(f'No data found to delete', ephemeral=True)