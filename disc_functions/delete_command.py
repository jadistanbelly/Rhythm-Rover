from variables import tree, user_audio_files # Change from variables to configs to run on your own bot
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
    user_id = str(interaction.user.id) # Get user ID
    intro_path, outro_path = user_audio_files[user_id] # Get intro and outro path
    try:
        if os.path.exists(intro_path): os.remove(intro_path) # Remove intro
        if os.path.exists(outro_path): os.remove(outro_path) # Remove outro
        del user_audio_files[user_id] # Remove user from keys
    except KeyError or FileNotFoundError:
        await interaction.response.send_message(f'You have no audio files to delete', ephemeral = True)
    sync_db()
    await interaction.response.send_message(f'Deleted!', ephemeral = True) # Tell user that operation was successful
