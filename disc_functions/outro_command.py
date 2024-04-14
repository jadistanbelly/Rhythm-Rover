import discord
from discord import app_commands
import os
from py_functions.download_audio import download_audio
from py_functions.totalseconds import totalseconds
import asyncio
from variables import Path, user_audio_files, audio_db, tree # Change from variables to configs to run on your own bot

# Define the download command
@tree.command(
    name="outro",
    description="Tell me what outro song you would like",
    #guilds=servers
)
# Provide instructions to user
@app_commands.describe(video_url = "Type your url",
                       start = "Where do you want to start the download?",
                       end = "Where do you want to end the download?")

# Create outro function
async def outro(interaction: discord.Interaction, video_url: str, start: str, end: str):
    ''' outro function for users to change outro audio'''
    # Convert and overwrite timestamps to only seconds
    start = totalseconds(start)
    end = totalseconds(end)
    try:
        # Check if timestamp is 10 sec or less
        if end-start <= 10:

            # Check if user already has an audio file if so delete before downloading a new one
            if str(interaction.user.id) in user_audio_files:
                try:
                    os.remove(user_audio_files[str(interaction.user.id)][1])
                    user_audio_files[str(interaction.user.id)][1] = None # Clear any saved filepath in dict
                except Exception:
                    pass

            # Defer response to user to get 15 min window for follow up message
            await interaction.response.defer(ephemeral = True)

            try:
                # Download the video
                audio_title = download_audio(video_url, Path, start, end)
            except Exception as e:
                await interaction.edit_original_response(content= e)

            # Insert User ID and path of outro
            if len(user_audio_files[str(interaction.user.id)]) < 2: # Check if user alread has an outro
                user_audio_files[str(interaction.user.id)].append(f'{Path}{audio_title}.mp3') # if not append
            else:
                user_audio_files[str(interaction.user.id)][1] = f'{Path}{audio_title}.mp3' # if so overwrite

            # Update Shelf DB
            audio_db['user_audio_paths'] = user_audio_files

            # Save changes immediately
            audio_db.sync()

            # Sleep for 3 seconds to ensure initial response window passes
            await asyncio.sleep(3) # Can probably be shortened some more

            # Respond back to user
            await interaction.edit_original_response(content="Your outro has been added")


        else:
            # Check if user already has an audio file if so delete before downloading a new one
            if str(interaction.user.id) in user_audio_files:
                try:
                    os.remove(user_audio_files[str(interaction.user.id)][1])
                    user_audio_files[str(interaction.user.id)][1] = None # Clear any saved filepath in dict
                except Exception:
                    pass

            # Overwrite user error of timestamp total higher than 10
            end = start+10

            # Defer response to user to get 15 min window for follow up message
            await interaction.response.defer(ephemeral = True)

            try:
                # Download the video
                audio_title = download_audio(video_url, Path, start, end)
            except Exception as e:
                await interaction.edit_original_response(content= e)

            # Insert User ID and path of outro
            if len(user_audio_files[str(interaction.user.id)]) < 2: # Check if user alread has an outro
                user_audio_files[str(interaction.user.id)].append(f'{Path}{audio_title}.mp3') # if not append
            else:
                user_audio_files[str(interaction.user.id)][1] = f'{Path}{audio_title}.mp3' # if so overwrite

            # Update Shelf DB
            audio_db['user_audio_paths'] = user_audio_files

            # Save changes immediately
            audio_db.sync()

            # Sleep for 3 seconds to ensure initial response window passes
            await asyncio.sleep(3) # Can probably be shortened some more

            # Respond back to user
            await interaction.edit_original_response(content="Your outro has been added")

    except asyncio.TimeoutError:
        await interaction.response.send_message("You took too long to respond. Please try again.",
                                                ephemeral = True)
