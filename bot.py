'''Import required modules'''
import disc_functions
from variables import bot, bot_token # Change from variables to configs to run on your own bot

# Identify bot login information
@bot.event
async def on_ready():
    print("Logged in as:",
          f"{bot.user.name} ({bot.user.id})")
    print("---------------------------------")

# Register voice state update event directly
@bot.event
async def on_voice_state_update(member, before, after):
    '''track if user joins voice channel'''
    await disc_functions.handle_voice_state_update(member, before, after)

# Run the bot
bot.run(bot_token)
