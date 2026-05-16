import disc_functions
from variables import bot, bot_token


@bot.event
async def on_ready():
    print("Logged in as:",
          f"{bot.user.name} ({bot.user.id})")
    print("---------------------------------")


@bot.event
async def on_voice_state_update(member, before, after):
    """Track voice state updates."""
    await disc_functions.handle_voice_state_update(member, before, after)


bot.run(bot_token)
