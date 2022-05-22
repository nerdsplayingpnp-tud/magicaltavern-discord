import os
import json
from discord.commands import Option
import discord
from discord.ext import commands
from discord.commands import (
    slash_command,
)
from src.sqlite.database_handler import Connection as Handler
from src.helper_functions import get_project_root, from_project_root, config_var, roles_var
import sqlite3

roles_path = os.path.join(get_project_root(), "/config/roles.json")  # why lol
with open(from_project_root('/config/roles.json'), encoding='utf-8') as roles_json:  # also just why lmfao
    __roles_dict__ = json.load(roles_json)
    id_role_admin = __roles_dict__['role-admin']
list_guilds = config_var('guilds')
import datetime


class DungeonMasterTools(commands.Cog):
    """
    TODO: Add Description
    """

    # Some utility commands.

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def check_admin(self=None):
        def predicate(ctx):
            return (commands.check_any(commands.has_role(id_role_admin),
                                       commands.has_permissions(
                                           administrator=True),
                                       commands.is_owner()))

        return commands.check(predicate)

    @slash_command(
        name='suggest-campaign',
        guild_ids=list_guilds,
    )
    @commands.has_role(roles_var('role-dm'))
    async def suggest_campaign(self,
                               ctx: discord.Interaction,
                               name: Option(str, "Der Name der Kampagne."),
                               description: Option(str, description="Beschreibt hier kurz die Kampagne",
                                                   name="beschreibung"),  # pylint: disable=C0301
                               min_players: Option(int, description="Wie viele Leute werden für die Kampagne "
                                                                    "mindestens benötigt? Min. 1, Max. 10",
                                                   min_value=1, max_value=10),  # pylint: disable=C0301
                               max_players: Option(int, description="Wie viele Leute können maximal an der Kampagne "
                                                                    "teilnehmen? Min. 3, Max. 10", min_value=3,
                                                   max_value=10),
                               complexity: Option(str, description="Gib an, wie komplex deine Kampagne in etwa ist.",
                                                  choices=["Einsteigerfreundlich", "Fortgeschritten",
                                                           "Sehr fortgeschritten"]),
                               place: Option(str, description="Wo wird deine Kampagne stattfinden?",
                                             choices=["Online", "Präsenz", "Beides"], name="ort"),
                               time: Option(str, description="Zu welcher Zeit soll das PNP ungefähr stattfinden?",
                                            name="zeit"),
                               content_warnings: Option(str, description="Gib hier explizite Contenthinweise an.",
                                                        name="content_warnungen"),
                               ruleset: Option(str, description="Welches Regelwerk verwendet die Kampagne?",
                                               name="regelwerk"),
                               type: Option(str, name="typ", choices=["Oneshot (1-2 Sessions)", "Kürzere Kampagne ("
                                                                                                "3-7 Sessions)",
                                                                      "Längere Kampagne (7+ Sessions)"],
                                            description="Ist deine Kampagne eher ein Oneshot oder eine längere "
                                                        "Kampagne?"),
                               language: Option(str, name="sprache", description="In welchen Sprachen wird dein "
                                                                                 "Abenteuer angeboten?",
                                                choices=["Englisch", "Deutsch", "Englisch & Deutsch"]),
                               character_creation: Option(str, name="charaktererstellung", description="Wie wird die "
                                                                                                       "Charaktererstellung gehandlet?"),
                               briefing: Option(str, name="briefing", description="Wie hast du vor deine "
                                                                                  "Spieler:innen zu briefen (Session "
                                                                                  "0 irl/online, per DM, "
                                                                                  "selbstständig)?"),
                               notes: Option(str, "Hier ist Platz für alles, was noch offen ist.",
                                             name="notizen_und_sonstiges"),
                               image_url: Option(str, description="Direktlink zu einem Bild, welches du einbetten "
                                                                  "möchtest.", required=False) = None
                               ):
        if image_url is None:
            image_url = "https://cdn.discordapp.com/avatars/959837234033475584/744a62cb7f9f8e94931e1400a6ea45f4.png" \
                        "?size=1024 "
        embed = discord.Embed(
            title=name,
            description=f"**Beschreibung:** {description}",
            color=0xDDA0DD
        )
        # Take all the info and send it as a fancy embed:
        embed.add_field(name="Minimal benötigte Anzahl an Spieler:innen", value=min_players)
        embed.add_field(name="Maximale Anzahl an Spieler:innen", value=max_players)
        embed.add_field(name="Komplexität", value=complexity)
        embed.add_field(name="Ort", value=place, inline=True)
        embed.add_field(name="Zeit", value=time, inline=True)
        embed.add_field(name="Contentwarnungen", value=content_warnings, inline=False)
        embed.add_field(name="Verwendetes Regelwerk", value=ruleset, inline=True)
        embed.add_field(name="Länge der Kampagne", value=type, inline=True)
        embed.add_field(name="Sprache", value=language, inline=True)
        embed.add_field(name="Richtlinien zur Charaktererstellung", value=character_creation, inline=False),
        embed.add_field(name="Briefing", value=briefing, inline=False)
        embed.add_field(name="Weitere Bemerkungen", value=notes, inline=False)
        embed.set_author(name=ctx.user.name)
        embed.set_image(url=image_url)
        await ctx.response.send_message(embed=embed)
        date = datetime.date.today()
        Handler.insert_into_campaigns(Handler.create_connection(), name, min_players, max_players, date.strftime("%m%d%Y"), None)

        # Insert the campaign into the database


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.

    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(DungeonMasterTools(bot))
