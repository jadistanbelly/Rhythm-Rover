from variables import bot 
from discord.ext import commands

# Define the sync command        
@bot.command()
@commands.is_owner() # Owner only
async def sync(ctx: commands.Context) -> None:
    """Sync commands"""
    synced = await ctx.bot.tree.sync() # Sync commands
    await ctx.send(f"Synced {len(synced)} commands globally") # Send message
