from variables import tree, bot 
from disc_functions.voice_events import audio_queue
import discord

# Define the kill command
@tree.command(
    name="kill",
    description="Clear Queue",
    #guilds=servers
)

async def kill(interaction):
    '''Command to clear queue and prevent spamming'''
    try:
        audio_queue.clear() # Clear queue
        voice_client = discord.utils.get(bot.voice_clients, guild=interaction.channel.guild) # Find where the bot is
        if voice_client.is_playing(): # Check if bot is playing
            voice_client.stop() # Stop the bot
        await interaction.response.send_message('Queue Cleared',
                                                ephemeral = True)
    except Exception as e:
        await interaction.response.send_message(f'Clearing failed. Error: {e}',
                                                ephemeral = True)
