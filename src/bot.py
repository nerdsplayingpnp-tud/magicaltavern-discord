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
from discord.ext import commands
from src.commands.dm_tools import PersistentView

load_dotenv()

if "TOKEN" not in environ:
    raise RuntimeError("TOKEN environment variable not set, exiting.")

__token__ = environ.get("TOKEN")

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents)
        self.persistent_views_added = False
    
    async def on_ready(self):
        if not self.persistent_views_added:
                # Register the persistent view for listening here.
                # Note that this does not send the view to any message.
                # In order to do this you need to first send a message with the View, which is shown below.
                # If you have the message_id you can also pass it as a keyword argument,
                # but for this example we don't have one.
                self.add_view(PersistentView(None))
                self.persistent_views_added = True
                
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        await bot.change_presence(activity=discord.Game("Die Taverne hat geöffnet!"))

bot = PersistentViewBot()



# Load all the cogs
bot.load_extension("src.commands.utility")
bot.load_extension("src.commands.dm_tools")
# Connect the bot to the discord api
bot.run(__token__)
