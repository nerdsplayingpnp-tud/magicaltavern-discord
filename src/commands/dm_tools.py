import os, json, datetime, discord, requests
from discord.commands import Option
from discord.ext import commands
from discord.commands import (
    slash_command,
)
from src.helper_functions import (
    api_var,
    get_project_root,
    from_project_root,
    config_var,
    roles_var,
    api_var,
    user_has_role_id,
    user_has_any_role,
)

roles_path = os.path.join(get_project_root(), "/config/roles.json")  # why lol
with open(
    from_project_root("/config/roles.json"), encoding="utf-8"
) as roles_json:  # also just why lmfao
    __roles_dict__ = json.load(roles_json)
    id_role_admin = __roles_dict__["role-admin"]
list_guilds = config_var("guilds")


class DungeonMasterTools(commands.Cog):
    """
    TODO: Add Description
    """

    # Some utility commands.

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        name="suggest-campaign",
        guild_ids=list_guilds,
    )
    async def suggest_campaign(
        self,
        ctx: discord.Interaction,
        name: Option(str, "Der Name der Kampagne."),
        description: Option(
            str, description="Beschreibt hier kurz die Kampagne", name="beschreibung"
        ),  # pylint: disable=C0301
        min_players: Option(
            int,
            description="Wie viele Leute werden für die Kampagne "
            "mindestens benötigt? Min. 1, Max. 10",
            min_value=1,
            max_value=10,
        ),  # pylint: disable=C0301
        max_players: Option(
            int,
            description="Wie viele Leute können maximal an der Kampagne "
            "teilnehmen? Min. 3, Max. 10",
            min_value=3,
            max_value=10,
        ),
        complexity: Option(
            str,
            description="Gib an, wie komplex deine Kampagne in etwa ist.",
            choices=["Einsteigerfreundlich", "Fortgeschritten", "Sehr fortgeschritten"],
        ),
        place: Option(
            str,
            description="Wo wird deine Kampagne stattfinden?",
            choices=["Online", "Präsenz", "Beides"],
            name="ort",
        ),
        time: Option(
            str,
            description="Zu welcher Zeit soll das PNP ungefähr stattfinden?",
            name="zeit",
        ),
        content_warnings: Option(
            str,
            description="Gib hier explizite Contenthinweise an.",
            name="content_warnungen",
        ),
        ruleset: Option(
            str,
            description="Welches Regelwerk verwendet die Kampagne?",
            name="regelwerk",
        ),
        type: Option(
            str,
            name="typ",
            choices=[
                "Oneshot (1-2 Sessions)",
                "Kürzere Kampagne (" "3-7 Sessions)",
                "Längere Kampagne (7+ Sessions)",
            ],
            description="Ist deine Kampagne eher ein Oneshot oder eine längere "
            "Kampagne?",
        ),
        language: Option(
            str,
            name="sprache",
            description="In welchen Sprachen wird dein " "Abenteuer angeboten?",
            choices=["Englisch", "Deutsch", "Englisch & Deutsch"],
        ),
        character_creation: Option(
            str,
            name="charaktererstellung",
            description="Wie wird die Charaktererstellung gehandlet?",
        ),
        briefing: Option(
            str,
            name="briefing",
            description="Wie hast du vor deine "
            "Spieler:innen zu briefen (Session "
            "0 irl/online, per DM, "
            "selbstständig)?",
        ),
        notes: Option(
            str,
            "Hier ist Platz für alles, was noch offen ist.",
            name="notizen_und_sonstiges",
        ),
        image_url: Option(
            str,
            description="Direktlink zu einem Bild, welches du einbetten " "möchtest.",
            required=False,
        ) = None,
    ):

        if not user_has_any_role(ctx, roles_var("role-dm")):
            await ctx.response.send_message(
                "Du siehst mir aber nicht wie ein:e Spielemeister:in aus... Ich hab' aber "
                "gehört dass die Leiter:innen dieser Taverne wieder anheuern! Schau mal "
                "drüben bei #dm-bewerbung vorbei!",
                ephemeral=True,
            )
            return

        data_dict = {
            "name": name,
            "dungeon_master": ctx.user.id,
            "description": description,
            "players_min": min_players,
            "players_max": max_players,
            "complexity": complexity,
            "place": place,
            "time": time,
            "content_warnings": content_warnings,
            "ruleset": ruleset,
            "campaign_length": type,
            "language": language,
            "character_creation": character_creation,
            "briefing": briefing,
            "notes": notes,
            "image_url": image_url,
        }

        apikey = api_var("token")
        api_url = config_var("api-url")
        api_port = config_var("api-port")
        response_key = requests.post(
            f"{api_url}:{api_port}/api/v1.0/campaigns/?apikey={apikey}",
            json=data_dict,
        )

        color = discord.Colour.random()
        embed = discord.Embed(
            title=name, description=f"**Beschreibung:** {description}", color=color
        )

        # Take all the info and send it as a fancy embed:
        embed.add_field(
            name="Minimal benötigte Anzahl an Spieler:innen", value=min_players
        )
        embed.add_field(name="Maximale Anzahl an Spieler:innen", value=max_players)
        embed.add_field(name="Komplexität", value=complexity)
        embed.add_field(name="Ort", value=place, inline=True)
        embed.add_field(name="Zeit", value=time, inline=True)
        embed.add_field(name="Contentwarnungen", value=content_warnings, inline=False)
        embed.add_field(name="Verwendetes Regelwerk", value=ruleset, inline=True)
        embed.add_field(name="Länge der Kampagne", value=type, inline=True)
        embed.add_field(name="Sprache", value=language, inline=True)
        embed.add_field(
            name="Richtlinien zur Charaktererstellung",
            value=character_creation,
            inline=False,
        ),
        embed.add_field(name="Briefing", value=briefing, inline=False)
        embed.add_field(name="Weitere Bemerkungen", value=notes, inline=False)
        embed.set_author(name=ctx.user.name)
        if image_url is not None:
            embed.set_image(url=image_url)
        # TODO: Change this
        await ctx.response.send_message(embed=embed)


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.

    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(DungeonMasterTools(bot))
