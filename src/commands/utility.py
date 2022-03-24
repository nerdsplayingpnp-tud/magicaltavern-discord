from discord.commands import (
    slash_command,
)
import discord
from discord.ext import commands
from logger.ownlogger import log
from utils import *
import os
import json

roles_path = os.path.join(get_project_root(), "/config/roles.json")
with open(from_project_root('/config/roles.json')) as roles_json:
    __roles_dict__ = json.load(roles_json)
    id_role_admin = __roles_dict__['role-admin']

list_guilds = config_var('guilds')


class UtilityCommands(commands.Cog):
    # Some utility commands.

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # check_admin is a decorator that returns as True, if the Context User is either the bot owner, has the admin_role configured in
    # config.json, or simply has administrator permissions.

    def check_admin():
        def predicate(ctx):
            return(commands.check_any(commands.has_role(id_role_admin), commands.has_permissions(administrator=True), commands.is_owner()))
        return commands.check(predicate)

    # Simple ping-command to check if the bot is still alive.

    @slash_command(
        name='ping',
        guild_ids=list_guilds)
    async def ping(self, ctx: commands.Context):
        await ctx.respond(f"Latenz: {round(self.bot.latency * 1000)}ms")

    # Manipulate the displayed Discord-Activity with this command.

    @slash_command(
        name='setstatus',
        guild_ids=list_guilds
    )
    @check_admin()
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Sets the activity status of the bot."""
        await self.bot.change_presence(activity=discord.Game(name=text))
        await ctx.respond('Aktion erfolgreich ausgeführt.')

    # Easy way to test new decorators, functions or anything else :)

    @slash_command(
        name='debug',
        guild_ids=list_guilds
    )
    @check_admin()
    async def debug(self, ctx: commands.Context):
        # This is how we get IDs from the Context: ctx.message.author.roles[1].id
        print('success')
        # This setup-function is needed to let discord.py load the cog
        await ctx.respond('Erfolg.')


def setup(bot: commands.Bot):
    bot.add_cog(UtilityCommands(bot))
