import discord
from discord.ext import commands
from logger.ownlogger import log


class UtilityCommands(commands.Cog):
    # Some utility commands.

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='latency')
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Latenz: {round(self.bot.latency * 1000)}ms")

    @commands.command(name='setstatus')
    async def setstatus(self, ctx: commands.Context, *, text: str):
        await self.bot.change_presence(activity=discord.Game(name=text))


# This setup-function is needed to let discord.py load the cog
def setup(bot: commands.Bot):
    bot.add_cog(UtilityCommands(bot))
