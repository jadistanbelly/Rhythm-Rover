import discord

from variables import audio_queue, bot, tree


# Define the kill command
@tree.command(
    name="kill",
    description="Clear Queue",
    #guilds=servers
)

async def kill(interaction):
    """Clear the playback queue and stop the current voice client."""
    try:
        audio_queue.clear()
        voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        await interaction.response.send_message("Queue Cleared", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(
            f"Clearing failed. Error: {e}",
            ephemeral=True,
        )
