"""
    IMPORTS:

    discord, discord.ext
        Used for: Literally everything discord-api related.

    logger.ownlogger: log
        Used for: logging, duh.

    helper_functions
        Used for: please see helper_functions.py docstrings for an explanation.
    """
import discord
from os import environ
from dotenv import load_dotenv
from src.logger.ownlogger import log
from src.helper_functions import from_project_root, config_var
from src.sqlite.database_initialiser import db_init


load_dotenv()

if "TOKEN" not in environ:
    raise RuntimeError("TOKEN environment variable not set, exiting.")

__token__ = environ.get("TOKEN")

db_init()  # Ensure the database tables exist
bot = discord.Bot()


@bot.event
async def on_ready():
    """Gets executed once the bot is logged in.
    """
    await bot.change_presence(activity=discord.Game('Die Taverne hat geöffnet!'))


# Load all the cogs
bot.load_extension("src.commands.utility")
bot.load_extension("src.commands.dm_tools")
# Connect the bot to the discord api
bot.run(__token__)
