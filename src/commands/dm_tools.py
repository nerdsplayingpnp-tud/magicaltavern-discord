import discord, requests
from discord.commands import Option
from discord.ext import commands
from discord.commands import (
    slash_command,
)
from src.helper_functions import get_var, user_has_any_role
from requests.exceptions import JSONDecodeError
import json

list_guilds = get_var("config/config.json", "guilds")
id_role_admin = get_var("config/roles.json", "role-admin")
token = get_var("config/apikey.json", "token")
api_url = get_var("config/config.json", "api-url")
api_port = get_var("config/config.json", "api-port")


def dict_key_by_value(dictionary: dict, search: any):
    for (
        key,
        value,
    ) in (
        dictionary.items()
    ):  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if value == search:
            return key


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
        player_id = interaction.user.id
        campaign_id = requests.get(
            f"{api_url}:{api_port}/api/v2.0/campaigns/from_message_id/{message_id}",
            headers={"token": token},
        ).json()
        campaign = requests.get(
            f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}",
            headers={"token": token},
        ).json()

        campaign_players = requests.get(
            f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}/players",
            headers={"token": token},
        ).json()

        campaign_full = len(campaign_players) >= campaign["players_max"]

        if str(player_id) in campaign_players:
            # Case: Player is already in the campaign.
            requests.put(
                f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}/players/remove/{player_id}",
                headers={"token": token},
            )
            await interaction.response.send_message(
                "Du wurdest aus der Kampagne ausgetragen!", ephemeral=True
            )
            return
        else:
            # Case: Player is not in the campaign...
            if campaign_full:
                # ...but the campaign is full
                await interaction.response.send_message(
                    "Diese Kampagne ist zur Zeit leider voll.", ephemeral=True
                )
                return
            # ...and the campaign is not full
            player_add_response = requests.put(
                f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}/players/add/{player_id}",
                headers={"token": token},
            )
            if player_add_response.status_code == 409:
                await interaction.response.send_message(
                    "Du kannst dich nicht in diese Kampagne eintragen.", ephemeral=True
                )
                return
            await interaction.response.send_message(
                "Du wurdest in die Kampagne eingeschrieben!", ephemeral=True
            )
            return


class DungeonMasterTools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        name="create-campaign",
        guild_ids=list_guilds,
        description="Erstelle eine neue Kampagne.",
    )
    async def create_campaign(
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
                "Kürzere Kampagne (3-7 Sessions)",
                "Längere Kampagne (7+ Sessions)",
            ],
            description="Ist deine Kampagne ein Oneshot oder eine längere " "Kampagne?",
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
            "Teile den Abenteurer\*innen mit, wann die Einschreibung für diese Kampagne eröffnet wird.",
            name="einschreibung_datum_zeit",
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
                "gehört dass die Leiter\*innen dieser Taverne wieder anheuern! Schau mal "
                "drüben bei #dm-bewerbung vorbei!",
                ephemeral=True,
            )
            return

        type_to_dict = {
            "Oneshot (1-2 Sessions)": 0,
            "Kürzere Kampagne (3-7 Sessions)": 1,
            "Längere Kampagne (7+ Sessions)": 2,
        }

        complexity_to_dict = {
            "Einsteigerfreundlich": 0,
            "Fortgeschritten": 1,
            "Sehr fortgeschritten": 2,
        }

        language_to_dict = {"Englisch": 0, "Deutsch": 1, "Englisch & Deutsch": 2}

        data_dict = {
            "name": name,
            "description": description,
            "players_min": min_players,
            "players_max": max_players,
            "complexity": complexity_to_dict[complexity],
            "place": place,
            "time": time,
            "content_warnings": content_warnings,
            "ruleset": ruleset,
            "campaign_length": type_to_dict[type],
            "language": language_to_dict[language],
            "character_creation": character_creation,
            "briefing": briefing,
            "notes": notes,
            "image_url": image_url,
        }

        response_key = requests.post(
            f"{api_url}:{api_port}/api/v2.0/campaigns/",
            json=data_dict,
            headers={"token": token},
        ).json()

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
        embed.add_field(
            name="Wann beginnt die Einschreibung?", value=notes, inline=False
        )
        embed.set_author(name=ctx.user.name)
        if image_url is not None:
            embed.set_image(url=image_url)
        # msg = await ctx.send(embed=embed, view=PersistentView())
        msg = await ctx.send(embed=embed)
        await ctx.response.send_message(
            f"✅ Die Kampagne wurde im System angelegt. Vergiss nicht, die Einschreibung mit `/activate {response_key}` freizuschalten, wenn die Zeit gekommen ist. Wenn du die ID deiner Kampagne vergisst, kannst du diese mit `/my-campaigns` wiederfinden!",
            ephemeral=True,
        )
        requests.post(
            f"{api_url}:{api_port}/api/v2.0/campaigns/{response_key}/message_id/{msg.id}",
            headers={"token": token},
        )
        requests.put(
            f"{api_url}:{api_port}/api/v2.0/campaigns/{response_key}/dm/add/{ctx.user.id}",
            headers={"token": token},
        )

        ### End of Embed Creation and sending ###

    @slash_command(
        name="my-campaigns",
        guild_ids=list_guilds,
        description="Zeige den Status der Kampagnen an, von welchen du DM bist.",
    )
    async def my_campaigns(self, ctx: discord.Interaction):
        user = ctx.user.id
        my_campaigns = json.loads(
            requests.get(
                f"{api_url}:{api_port}/api/v2.0/users/{user}/dms_campaigns/",
                headers={"token": token},
            ).content.decode("utf-8")
        )
        embed = discord.Embed(
            title="Meine Kampagnen",
            description="**Hier hast du eine Übersicht über deine Kampagnen.**",
        )
        for campaign in my_campaigns:
            name = my_campaigns[campaign]["name"]
            id = my_campaigns[campaign]["id"]
            players_min = my_campaigns[campaign]["players_min"]
            players_max = my_campaigns[campaign]["players_max"]
            players = []
            players_current = int()
            try:
                players = requests.get(
                    f"{api_url}:{api_port}/api/v2.0/campaigns/{id}/players",
                    headers={"token": token},
                ).json()
                players_current = len(players)
            except JSONDecodeError:
                players_current = 0
            players_str = ""
            for player in players:
                players_str += "<@" + player + ">, "
            embed.add_field(
                name=name,
                value=f"**ID:** {id}\n **Momentane anz. Spieler\*innen:** {players_current}/{players_max}\n **Minimale anz. Spieler\*innen:** {players_min}\n **Spieler\*innen**: {players_str[:-2:]}",
                inline=False,
            )
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @slash_command(
        name="activate",
        guild_ids=list_guilds,
        description="Gib eine Kampagne zur Einschreibung frei.",
    )
    async def activate(
        self,
        ctx: discord.Interaction,
        campaign_id: Option(
            int,
            description="Gib die ID der Kampagne an, welche du zur Einschreibung freigeben möchtest.",
        ),
    ):
        user = ctx.user.id
        user_campaigns = requests.get(
            f"{api_url}:{api_port}/api/v2.0/users/{user}/dms_campaigns/",
            headers={"token": token},
        ).json()

        for campaign_iter in user_campaigns:
            if campaign_id == user_campaigns[campaign_iter]["id"]:
                response_activate = requests.put(
                    f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}/allow_enrollement",
                    headers={"token": token},
                )
                if response_activate.status_code == 409:
                    return ctx.response.send_message(
                        "Die Kampagne ist bereits aktiv.", ephemeral=True
                    )
                campaign = requests.get(
                    f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}",
                    headers={"token": token},
                ).json()
                old_message = await ctx.fetch_message(campaign["message_id"])
                await old_message.delete()

                if not user_has_any_role(ctx, get_var("config/roles.json", "role-dm")):
                    await ctx.response.send_message(
                        "Du siehst mir aber nicht wie ein:e Spielemeister:in aus... Ich hab' aber "
                        "gehört dass die Leiter\*innen dieser Taverne wieder anheuern! Schau mal "
                        "drüben bei #dm-bewerbung vorbei!",
                        ephemeral=True,
                    )
                    return

                type_to_dict = {
                    "Oneshot (1-2 Sessions)": 0,
                    "Kürzere Kampagne (3-7 Sessions)": 1,
                    "Längere Kampagne (7+ Sessions)": 2,
                }

                complexity_to_dict = {
                    "Einsteigerfreundlich": 0,
                    "Fortgeschritten": 1,
                    "Sehr fortgeschritten": 2,
                }

                language_to_dict = {
                    "Englisch": 0,
                    "Deutsch": 1,
                    "Englisch & Deutsch": 2,
                }

                data_dict = {
                    "name": campaign["name"],
                    "description": campaign["description"],
                    "players_min": campaign["players_min"],
                    "players_max": campaign["players_max"],
                    "complexity": dict_key_by_value(
                        complexity_to_dict, campaign["complexity"]
                    ),
                    "place": campaign["place"],
                    "time": campaign["time"],
                    "content_warnings": campaign["content_warnings"],
                    "ruleset": campaign["ruleset"],
                    "campaign_length": dict_key_by_value(
                        type_to_dict, campaign["campaign_length"]
                    ),
                    "language": dict_key_by_value(
                        language_to_dict, campaign["language"]
                    ),
                    "character_creation": campaign["character_creation"],
                    "briefing": campaign["briefing"],
                    "notes": campaign["notes"],
                    "image_url": campaign["image_url"],
                }

                ### Embed Creation and sending ###
                # The code here is absolutely mindless.

                color = discord.Colour.random()
                embed = discord.Embed(
                    title=data_dict["name"],
                    description="**Beschreibung:** " + data_dict["description"],
                    color=color,
                )

                # Take all the info and send it as a fancy embed:
                embed.add_field(
                    name="Minimal benötigte Anzahl an Spieler:innen",
                    value=data_dict["players_min"],
                )
                embed.add_field(
                    name="Maximale Anzahl an Spieler:innen",
                    value=data_dict["players_max"],
                )
                embed.add_field(name="Komplexität", value=data_dict["complexity"])
                embed.add_field(name="Ort", value=data_dict["place"], inline=True)
                embed.add_field(name="Zeit", value=data_dict["time"], inline=True)
                embed.add_field(
                    name="Contentwarnungen",
                    value=data_dict["content_warnings"],
                    inline=False,
                )
                embed.add_field(
                    name="Verwendetes Regelwerk",
                    value=data_dict["ruleset"],
                    inline=True,
                )
                embed.add_field(
                    name="Länge der Kampagne",
                    value=data_dict["campaign_length"],
                    inline=True,
                )
                embed.add_field(name="Sprache", value=data_dict["ruleset"], inline=True)
                embed.add_field(
                    name="Richtlinien zur Charaktererstellung",
                    value=data_dict["character_creation"],
                    inline=False,
                ),
                embed.add_field(
                    name="Briefing", value=data_dict["briefing"], inline=False
                )
                embed.add_field(
                    name="Wann beginnt die Einschreibung?",
                    value=data_dict["notes"],
                    inline=False,
                )
                embed.set_author(name=ctx.user.name)
                if data_dict["image_url"] != "None":
                    embed.set_image(url=data_dict["image_url"])
                msg = await ctx.send(embed=embed, view=PersistentView())
                await ctx.response.send_message(
                    f"✅ Die Einschreibung zur Kampagne wurde aktiviert. Den aktuellen Status der Kampagne kannst du mit `/my-campaigns` einsehen.",
                    ephemeral=True,
                )
                requests.post(
                    f"{api_url}:{api_port}/api/v2.0/campaigns/{campaign_id}/message_id/{msg.id}",
                    headers={"token": token},
                )


def setup(bot: discord.Bot):
    """This setup function is needed by pycord to "link" the cog to the bot.

    Args:
        bot (commands.Bot): the Bot-object.
    """
    bot.add_cog(DungeonMasterTools(bot))
