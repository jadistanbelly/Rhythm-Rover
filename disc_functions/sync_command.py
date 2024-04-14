from variables import tree, Owner, servers, bot # Change from variables to configs to run on your own bot
from discord.ext import commands
# Define the sync command
@tree.command(
    name="sync",
    description="Owner only",
    #guilds=servers
)

async def sync(interaction):
    '''Owner only command to sync command trees in all servers that bot is deployed in'''
    if interaction.user.id == Owner:
        synced = await tree.sync()
        await interaction.response.send_message(f'Synced {len(synced)} commands globally',
                                                ephemeral = True)
    else:
        await interaction.response.send_message('You must be the owner to use this command!',
                                                ephemeral = True)
        
