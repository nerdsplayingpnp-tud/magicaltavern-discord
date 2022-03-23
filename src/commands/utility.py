import discord
from discord.ext import commands
from logger.ownlogger import log
from utils import *
import os
import json

roles_path = os.path.join(get_project_root(), "/config/roles.json")
with open(from_project_root('/config/roles.json')) as roles_json:
    roles_dict = json.load(roles_json)
    id_role_admin = roles_dict['role-admin']


class UtilityCommands(commands.Cog):
    # Some utility commands.

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def check_admin_role(ctx: commands.Context):
        # TODO: This is not working! I just wanted to make a commit again
        return ctx.message.author.id == id_role_admin

    @commands.command(name='latency')
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Latenz: {round(self.bot.latency * 1000)}ms")

    @commands.command(name='setstatus')
    @commands.check(check_admin_role)
    async def setstatus(self, ctx: commands.Context, *, text: str):
        await self.bot.change_presence(activity=discord.Game(name=text))

    @commands.command(name='debug')
    async def debug(self, ctx: commands.Context):
        print(id_role_admin)


# This setup-function is needed to let discord.py load the cog
def setup(bot: commands.Bot):
    bot.add_cog(UtilityCommands(bot))
