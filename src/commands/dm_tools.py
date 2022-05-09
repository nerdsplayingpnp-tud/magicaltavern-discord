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
from discord.commands import Option
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
        guild_ids=list_guilds,
    )
    # Notizen
    @commands.has_role(roles_var('role-dm'))
    async def suggest_campaign(self,  # pylint: disable=R0913
                               ctx: discord.Interaction,
                               name: Option(str, "Der Name der Kampagne."),
                               description: Option(str, description="Beschreibt hier kurz die Kampagne"),  # pylint: disable=C0301
                               min_players: Option(int, description="Wie viele Leute werden für die Kampagne mindestens benötigt? Min. 1, Max. 10", min_value=1, max_value=10),  # pylint: disable=C0301
                               max_players: Option(int, description="Wie viele Leute können maximal an der Kampagne teilnehmen? Min. 3, Max. 10", min_value=3, max_value=10),  # pylint: disable=C0301
                               content_warnings: Option(str, description="Gib hier explizite Contenthinweise an."),
                               ruleset: Option(str, description="Welches Regelwerk verwendet die Kampagne?", name="regelwerk"),
                               type: Option(str, name="typ", choices=["Oneshot (1-2 Sessions)", "Kürzere Kampagne (3-7 Sessions)", "Längere Kampagne (7+ Sessions)"], description="Ist deine Kampagne eher ein Oneshot oder eine längere Kampagne?"),
                               language: Option(str, name="sprache", description="In welchen Sprachen wird dein Abenteuer angeboten?", choices=["Englisch", "Deutsch", "Englisch & Deutsch"]),
                               character_creation: Option(str, name="charaktererstellung", description="Wie wird die Charaktererstellung gehandlet?"),
                               notes: Option(str, "Hier ist Platz für alles, was noch offen ist.", name="notizen_und_sonstiges"),
                               image_url: Option(str, description="Direktlink zu einem Bild, welches du einbetten möchtest.", required=False) = None
                               ):

        """callback (suggest-campaign) does what you think it does: You can suggest a campaign to
        your players.

        Args:
            ctx (discord.Interaction): Discord Interaction
        """
        if image_url is None:
            image_url = "https://cdn.discordapp.com/avatars/959837234033475584/744a62cb7f9f8e94931e1400a6ea45f4.png?size=1024"
        embed = discord.Embed(
            title=name,
            description=f"**Beschreibung:** {description}",
            color=0xDDA0DD
        )
        embed.add_field(name="Minimal benötigte Anzahl an Spieler:innen", value=min_players)
        embed.add_field(name="Maximale Anzahl an Spieler:innen", value=max_players)
        embed.add_field(name="Contentwarnungen", value=content_warnings, inline=False)
        embed.add_field(name="Verwendetes Regelwerk", value=ruleset, inline=True)
        embed.add_field(name="Länge der Kampagne", value=type, inline=True),
        embed.add_field(name="Sprache", value=language, inline=True),
        embed.add_field(name="Richtlinien zur Charaktererstellung", value=character_creation, inline=False),
        embed.add_field(name="Weitere Bemerkungen", value=notes, inline=False),
        embed.set_author(name=ctx.user.name)
        embed.set_image(url=image_url)
        await ctx.response.send_message(embed=embed)


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.

    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(DungeonMasterTools(bot))
