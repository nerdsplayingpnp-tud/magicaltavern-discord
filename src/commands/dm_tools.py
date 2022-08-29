from urllib import response
import discord, requests
from discord.commands import Option
from discord.ext import commands
from discord.commands import (
    slash_command,
)
from src.helper_functions import get_var, user_has_any_role
import json

list_guilds = get_var("config/config.json", "guilds")
id_role_admin = get_var("config/roles.json", "role-admin")


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # When the confirm button is pressed, set the inner value
    # to `True` and stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(
        label="Einschreiben/Austragen",
        style=discord.ButtonStyle.green,
        custom_id=f"persistent_view:campaigns",
    )
    async def confirm_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        message_id = interaction.message.id
        apikey = get_var("config/apikey.json", "token")
        api_url = get_var("config/config.json", "api-url")
        api_port = get_var("config/config.json", "api-port")
        player = str(interaction.user.id)
        get_db_key = requests.get(
            f"{api_url}:{api_port}/api/v1.0/message_keys/{message_id}"
        ).text[1:7]
        response_bool = requests.put(
            f"{api_url}:{api_port}/api/v1.0/campaigns/{get_db_key}/player/?apikey={apikey}&player={player}"
        )
        if response_bool.status_code == 409:
            await interaction.response.send_message(
                "Diese Kampagne ist zur Zeit leider voll.", ephemeral=True
            )
        if response_bool.text == "True":
            await interaction.response.send_message(
                "Du wurdest aus der Kampagne ausgetragen!", ephemeral=True
            )
            return
        elif response_bool.text == "False":
            await interaction.response.send_message(
                "Du bist in die Kampagne eingeschrieben!", ephemeral=True
            )


class DungeonMasterTools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # This is the slash command to suggest a campaign. It is really long, because it has a lot of
    # arguments. These arguments then get POSTed into the magicaltavern-api to store the campaign,
    # and then sent as an embed.

    @slash_command(
        name="suggest-campaign",
        guild_ids=list_guilds,
        description="Schlage als DM eine neue Kampagne vor.",
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

        # Abort if the user that issued the command is not a dungeon master
        if not user_has_any_role(ctx, get_var("config/roles.json", "role-dm")):
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

        apikey = get_var("config/apikey.json", "token")
        api_url = get_var("config/config.json", "api-url")
        api_port = get_var("config/config.json", "api-port")
        response_key = requests.post(
            f"{api_url}:{api_port}/api/v1.0/campaigns/?apikey={apikey}",
            json=data_dict,
        ).text.replace('"', "")[0:6]

        ### Embed Creation and sending ###
        # The code here is absolutely mindless.

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
        msg = await ctx.send(embed=embed, view=PersistentView())
        msg_id = msg.id
        await ctx.response.send_message(
            "✅ Die Kampagne wurde im System angelegt und erfolgreich gesendet.",
            ephemeral=True,
        )
        requests.put(
            f"{api_url}:{api_port}/api/v1.0/campaigns/{response_key}/has_view/?apikey={apikey}"
        )

        requests.post(
            f"{api_url}:{api_port}/api/v1.0/message_keys/?apikey={apikey}&messageid={msg_id}&db_key={response_key}"
        )

        ### End of Embed Creation and sending ###

    @slash_command(
        name="my-campaigns",
        guild_ids=list_guilds,
    )
    async def my_campaigns(self, ctx: discord.Interaction):
        apikey = get_var("config/apikey.json", "token")
        api_url = get_var("config/config.json", "api-url")
        api_port = get_var("config/config.json", "api-port")
        user = ctx.user.id
        my_campaigns = json.loads(
            requests.get(
                f"{api_url}:{api_port}/api/v1.0/campaigns/dm/{user}/?apikey={apikey}"
            ).content.decode("utf-8")
        )
        embed = discord.Embed(
            title="Meine Kampagnen",
            description="**Hier hast du eine Übersicht über deine Kampagnen.**",
        )
        for campaign in my_campaigns:
            campaign_dict = json.loads(
                requests.get(
                    f"{api_url}:{api_port}/api/v1.0/campaigns/{campaign}/?apikey={apikey}"
                ).content.decode("utf-8")
            )
            name = campaign_dict["name"]
            players_min = campaign_dict["players_min"]
            players_max = campaign_dict["players_max"]
            player_current = campaign_dict["players_current"]
            players = campaign_dict["players"]
            players_str = ""
            for player in players:
                players_str += "<@" + player + ">, "
            players_str[:-2:]
            embed.add_field(
                name=name,
                value=f"**Momentane anz. Spieler\*innen:** {player_current}/{players_max}\n **Minimale anz. Spieler\*innen:** {players_min}\n **Spieler\*innen**: {players_str}",
                inline=False,
            )
        await ctx.response.send_message(embed=embed, ephemeral=True)


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.

    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(DungeonMasterTools(bot))
