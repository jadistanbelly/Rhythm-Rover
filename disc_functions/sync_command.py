from variables import tree, Owner # Change from variables to configs to run on your own bot

# Define the sync command
@tree.command(
    name="sync",
    description="Owner only",
    #guilds=servers
)

async def sync(interaction):
    '''Owner only command to sync command trees in all servers that bot is deployed in'''
    if interaction.user.id == Owner:
        await tree.sync()
        await interaction.response.send_message('Command tree synced.',
                                                ephemeral = True)
    else:
        await interaction.response.send_message('You must be the owner to use this command!',
                                                ephemeral = True)