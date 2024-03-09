import discord
import asyncio

# Initialize the bot with intents (required for certain events)
intents = discord.Intents.default()
intents.voice_states = True  # Enable voice state events
client = discord.Client(intents=intents)

# Dictionary to map user IDs to audio file paths
user_audio_files = {
    "426031900633858048": "C:\\Users\\jadis\\OneDrive\\discord_bots\\ringmaster_riff\\audio\\johncena.mp3", # Jad
    "169183728277389312": "C:\\Users\\jadis\\OneDrive\\discord_bots\\ringmaster_riff\\audio\\undertaker.mp3", # Gogo
    "169178004684144650": "C:\\Users\\jadis\\OneDrive\\discord_bots\\ringmaster_riff\\audio\\reymysterio.mp3", # Hamood
    "304642517343928321": "C:\\Users\\jadis\\OneDrive\\discord_bots\\ringmaster_riff\\audio\\tripleh.mp3", # Ahmad
    "169793619908231168": "C:\\Users\\jadis\\OneDrive\\discord_bots\\ringmaster_riff\\audio\\randyorton.mp3", # Scott
    "641995250067570719": "C:\\Users\\jadis\\OneDrive\\discord_bots\\ringmaster_riff\\audio\\batista.mp3" # Farris
    # Add more user IDs and corresponding audio files as needed
}

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} ({client.user.id})")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel:  # User joined a voice channel
            user_id = str(member.id)
            if user_id in user_audio_files:
                audio_file_path = user_audio_files[user_id]
                vc = await after.channel.connect()
                vc.play(discord.FFmpegOpusAudio(executable= "C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe", source = audio_file_path))
                #vc.play(discord.FFmpegPCMAudio(executable= "C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe",source = audio_file_path))
                while vc.is_playing():
                    await asyncio.sleep(1)
                await vc.disconnect()

# Run the bot
client.run("MTIxNTgzMTU2NTEwMDM4ODM4Mg.GhwKLu.Q_zzzlPZ7KbkwoYU-XMVf7-8avbMJTqeyNyK10")
