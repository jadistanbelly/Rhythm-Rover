from variables import tree, user_audio_files # Change from variables to configs to run on your own bot
from discord import app_commands
import discord
import os
from py_functions.sync_db import sync_db
@tree.command(
    name="delete",
    description="Use only if you no longer want an intro or outro or both"
    #guilds=servers
)
@app_commands.describe(choice="Use /intro or /outro if you want to replace")
@app_commands.choices(choice=[
    app_commands.Choice(name="intro", value="intro"),
    app_commands.Choice(name="outro", value="outro"),
    app_commands.Choice(name="both", value="both")
])
async def delete(interaction: discord.Interaction, choice: str):
    '''Command to delete user intro and/or outro'''
    try:
        # Create readable variables 
        user_id = str(interaction.user.id) # Get user ID
        intro_path = user_audio_files[user_id][0] # First value indicating intro
        outro_path = user_audio_files[user_id][1] # Second value indicating outro


        if choice == 'intro' and intro_path is not None: # If user wants to delete intro
            if intro_path == outro_path: # Check if user selected the same audio for both
                user_audio_files[user_id][0]= None # Clear any saved filepath in dict
                sync_db() # Update database
                await interaction.response.send_message(f'Deleted intro{intro_path}',
                                                        ephemeral=True) # Tell user that intro was deleted
            elif intro_path != outro_path: # Check if user selected different audio for both
                os.remove(intro_path) # Delete intro file
                user_audio_files[user_id][0]= None # Clear any saved filepath in dict
                sync_db() # Update database
                await interaction.response.send_message('Deleted intro',
                                                        ephemeral=True) # Tell user that intro was deleted
        elif choice == 'outro' and outro_path is not None: # If user wants to delete outro
            if intro_path == outro_path: # Check if user selected the same audio for both
                user_audio_files[user_id][1]= None # Clear any saved filepath in dict
                sync_db() # Update database
                await interaction.response.send_message('Deleted outro',
                                                        ephemeral=True) # Tell user that outro was deleted
            elif intro_path != outro_path: # Check if user selected different audio for both
                os.remove(outro_path) # Delete outro file
                user_audio_files[user_id][1]= None # Clear any saved filepath in dict
                sync_db() # Update database
                await interaction.response.send_message('Deleted outro',
                                                    ephemeral=True)
        elif choice == 'both' and outro_path is not None and intro_path is not None: # If user wants to delete both
            if intro_path == outro_path: # Check if user selected the same audio for both
                os.remove(intro_path) # Delete intro file
                del user_audio_files[user_id] # Delete key/value pair in dict
                sync_db() # Update database
                await interaction.response.send_message('Deleted both intro and outro',
                                                        ephemeral = True) # Tell user that both were deleted
            elif intro_path != outro_path: # Check if user selected different audio for both
                os.remove(intro_path) # Delete intro file
                os.remove(outro_path) # Delete outro file
                del user_audio_files[user_id] # Delete key/value pair in dict
                sync_db() # Update database
                await interaction.response.send_message('Deleted both intro and outro',
                                                        ephemeral = True) # Tell user that both were deleted
        else:
            raise KeyError # Raise error if user does not have the choice they picked
    except KeyError or IndexError or FileNotFoundError: # Catch error if user does not have the choice they picked
        await interaction.response.send_message(f'You do not have {choice} to delete',
                                                ephemeral = True)