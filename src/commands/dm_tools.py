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
from discord.commands import Option
import os
import json
import discord
from discord.ext import commands
from discord.commands import (
    slash_command,
)
from helper_functions import get_project_root, from_project_root, config_var, roles_var  # pylint: disable=E0401

roles_path = os.path.join(get_project_root(), "/config/roles.json")
with open(from_project_root('/config/roles.json'), encoding='utf-8') as roles_json:
    __roles_dict__ = json.load(roles_json)
    id_role_admin = __roles_dict__['role-admin']

list_guilds = config_var('guilds')


class DungeonMasterTools(commands.Cog):
    """
    TODO: Add Description
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

    # The following behaviour is expected:
    # 1: Find out how much demand there is for a specific campaign. A DM can set how many people the
    # campaign is designed for, and how many groups they are willing to take.
    # 2: After this surveying period, if the requirements for at least one group are met, the DM can
    # the people who reacted with "I'm interested" get notified to vote for a date and time. the DM
    # can already withdraw certain weekday/time-combinations from the pool beforehand.
    # 3: After at least 24h, the DM gets notified and asked to pick a weekday/time combo. If the DM
    # allows multiple groups for one campaign, they can select multiple days on which campaign will
    # take place.
    # 4: The bot will now assign people to the group or groups. People get put in a queue the moment
    # they select that they're interested in the campaign. The group-assignment respects this queue.
    # 5: The roles and channels get created now. If a player leaves a group for some reason, the
    # next person from the queue gets notified and asked if they'd still like to join the campaign.
    # 6: When the campaign is eventually over, the DM can close the channels. All Roles and channels
    # get archived/deleted.

    @slash_command(
        name='suggest-campaign',
        guild_ids=list_guilds
    )
    @commands.has_role(roles_var('role-dm'))
    async def callback(self,
                       ctx: discord.Interaction,
                       name: Option(str, "Der Name der Kampagne."),
                       description: Option(str,
                                           "Beschreibe deine Kampagne hier kurz. Worum geht es? Weniger als 1800 Zeichen."),
                       min_players: Option(int, "Wie viele Leute werden für die Kampagne mindestens benötigt?", min_value=3,
                                           max_value=10),
                       max_players: Option(
                           int, "Wie viele Leute können maximal an der Kampagne teilnehmen?", min_value=5, max_value=10),
                       content_warnings: Option(
                           str, "Gib hier explizite Contenthinweise an.")
                       ):
        await ctx.response.send_message(f"{name}, {description}, {min_players}, {max_players}, {content_warnings}")


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.

    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(DungeonMasterTools(bot))
