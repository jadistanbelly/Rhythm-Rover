from variables import tree, Owner # Change from variables to configs to run on your own bot
from disc_functions.voice_events import audio_queue

# Define the kill command
@tree.command(
    name="kill",
    description="Clear Queue",
    #guilds=servers
)

async def kill(interaction):
    '''Owner only command to clear queue and prevent spamming'''
    if interaction.user.id == Owner:
        try:
            audio_queue.clear() # Clear queue
            await interaction.response.send_message('Queue Cleared',
                                                    ephemeral = True)
        except Exception as e:
            await interaction.response.send_message(f'Clearing failed. Error: {e}',
                                                    ephemeral = True)
    else:
        await interaction.response.send_message('You must be the owner to use this command!',
                                                ephemeral = True)