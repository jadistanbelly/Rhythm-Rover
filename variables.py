import os
import shelve
from collections import deque
from pathlib import Path as FilePath

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _optional_int_env(name: str) -> int | None:
    value = os.getenv(name)
    if not value:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer") from exc


def _optional_guilds(*names: str) -> list[discord.Object]:
    guilds = []
    for name in names:
        guild_id = _optional_int_env(name)
        if guild_id is not None:
            guilds.append(discord.Object(id=guild_id))
    return guilds


def _audio_path() -> str:
    audio_dir = FilePath(os.getenv("AUDIO_DIR", "audio"))
    return f"{audio_dir.as_posix().rstrip('/')}/"


outro_trigger = int(os.getenv("OUTRO_TRIGGER_SECONDS", "11"))
Path = _audio_path()

Owner = _optional_int_env("OWNER")

audio_queue = deque(maxlen=3)  # Set the queue limit to 3


def load_audio_files():
    """Load audio files from database, ensuring fresh data"""
    with shelve.open("audio_paths") as db:
        return dict(db.get("user_audio_paths", {}))


user_audio_files = load_audio_files()

ffmpeg_path = (
    "/usr/bin/ffmpeg"
    if os.name == "posix"
    else "C:\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe"
)

bot_token = _required_env("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot_options = {}
if Owner is not None:
    bot_options["owner_id"] = Owner

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
    **bot_options,
)
tree = bot.tree

servers = _optional_guilds("PRSSERVER", "FRSERVER")
server = servers[0] if servers else None
