# pylint: disable=R0201, R0801

"""
IMPORTS:
os
    Used for:
        Filesystem access and paths
json
    Used for:
        opening and parsing the files in /config
discord.commands, discord, discord.ext
    Used for:
        literally everything discord-api related
utils
    Used for:
        these are my own functions that i added for various reasons. see utils docs.
    """
import os
import json
from discord.commands import (
    slash_command,
)
import discord
from discord.ext import commands
from src.helper_functions import get_project_root, from_project_root, config_var


roles_path = os.path.join(get_project_root(), "/config/roles.json")
with open(from_project_root('/config/roles.json'), encoding='utf-8') as roles_json:
    __roles_dict__ = json.load(roles_json)
    id_role_admin = __roles_dict__['role-admin']

list_guilds = config_var('guilds')


class UtilityCommands(commands.Cog):
    """
    UtilityCommands houses all the utility commands.
    Utility Commands are commands that are nice to have, but not essential to complete the bots'
    actual goal.
    """

    # Some utility commands.

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        name='debug',
        guild_ids=list_guilds
    )
    async def debug(self, ctx: commands.Context):
        """A debug function that can be used for anything
        Args:
            ctx (commands.Context): The pycord-context object (passed automatically)
        """
        # This is how we get IDs from the Context: ctx.message.author.roles[1].id
        print('success')
        # This setup-function is needed to let discord.py load the cog
        await ctx.respond('Erfolg.')


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.
    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(UtilityCommands(bot))
