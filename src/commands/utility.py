# pylint: disable=R0201

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
from utils import get_project_root, from_project_root, config_var


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

    def check_admin(self=None):  # Self gets passed because pylint wants it. i'm probably doing
        # this wrong, but it cannot be that stupid if it works!
        """"check_admin() gets used as a predicate to check for all the possible conditions that
        would make a user an 'admin'-type user. The predicate returns True, if the Context User
        is either the bot owner, has the admin_role configured in
        config.json, or simply has administrator permissions.
        """
        def predicate(ctx):
            # ctx NEEDS to be passed to this predicate, because pycord demands it. The following
            # 2 lines are dedicated to remove a pylint warning.
            use_ctx = ctx
            ctx = use_ctx  # i hate this.
            return(commands.check_any(commands.has_role(id_role_admin),
                                      commands.has_permissions(
                                          administrator=True),
                                      commands.is_owner()))
        return commands.check(predicate)

    @slash_command(
        name='ping',
        guild_ids=list_guilds)
    async def ping(self, ctx: commands.Context):
        """Simple ping-command to check if the bot is still alive.

        Args:
            ctx (commands.Context): The pycord-context object (passed automatically)
        """
        await ctx.respond(f"Latenz: {round(self.bot.latency * 1000)}ms")

    @slash_command(
        name='setstatus',
        guild_ids=list_guilds
    )
    @check_admin()
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Manipulate the displayed Discord-Activity with this command.

        Args:
            ctx (commands.Context): The pycord-context object (passed automatically)
            text (str): The text that you'd like the bot to display as its' "Playing"-message.
        """
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.respond('Aktion erfolgreich ausgeführt.')

    # Easy way to test new decorators, functions or anything else :)

    @slash_command(
        name='debug',
        guild_ids=list_guilds
    )
    @check_admin()
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
