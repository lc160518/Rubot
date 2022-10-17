# bot.py
import os

import discord
from dotenv import load_dotenv
import random

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} im in')


joining = None
players = {}  # voor de dictiony
spelers = []  # voor de permissions
roleNumbers = []
playerNames = []
rolesList = []
lovers = []
already_joined_amount = 0
testing = False
done = None


@client.event
async def on_message(message):
    message.content = message.content.lower()
    global testing

    if client.user == message.author:
        return

    if message.content.startswith("start weerwolven"):
        await startup(message)

    global created_channels
    text_channel_list = []
    if message.content.startswith("delete channels"):
        for channel in message.guild.text_channels:
            text_channel_list.append(channel)
        for channel in text_channel_list:
            if channel.name in created_channels:
                await channel.delete()

    if message.content.startswith("reveal"):
        await permissies(message)

    if message.content.startswith("meesa cupido"):
        spelers.append(message.author.name.lower())
        await cupido(message)


created_channels = []
possible_channels = ["main_channel", "weerwolf_channel", "burger_channel", "ziener_channel", "heks_channel",
                     "jager_channel",
                     "cupido_channel", "meisje_channel", "dood_channel"]


async def startup(s):
    global joining
    global players
    global spelers
    global already_joined_amount
    global done

    overwrites = {
        s.guild.default_role: discord.PermissionOverwrite(view_channel=False)}

    for e in range(0, len(possible_channels)):
        await s.guild.create_text_channel(name=possible_channels[e], reason="startup", overwrites=overwrites)
        created_channels.append(possible_channels[e])

    main_channel = discord.utils.get(s.guild.text_channels, name="main_channel")

    main_over = discord.PermissionOverwrite()
    main_over.view_channel = True

    await main_channel.set_permissions(s.guild.default_role, overwrite=main_over)
    await main_channel.send("Stuur \"ik\" om mee te doen!")

    while len(players) < 25:
        def check(m):
            return client.user != s.author \
                   and m.content.startswith("ik") \
                   or m.content.startswith("disable joining") \
                   or m.content.startswith("force stop")

        msg = await client.wait_for("message", check=check)

        if msg.author.id not in players and msg.content.startswith("ik") and msg.channel == main_channel:
            players.update({msg.author.id: "geen rol"})
            spelers.append(msg.author.name.lower())
            await msg.channel.send("<@{.author.id}> joined".format(msg))

        if msg.author in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send("<@{.author.id}> already joined".format(msg))

        if msg.content.startswith("disable joining") and len(players) < 6:
            await msg.channel.send("Er zijn niet genoeg spelers, mensen kunnen nogsteeds joinen")

        if msg.content.startswith("disable joining") and len(players) >= 6:
            await msg.channel.send("Mensen kunnen niet meer joinen!")
            break

        if msg.content.startswith("force stop"):
            await msg.channel.send("Forced stopped joining")
            await msg.channel.send(players)
            force_stopped = True
            break

    if not force_stopped:
        role_selector()
    if not force_stopped:
        await pre_game(main_channel)
    if not force_stopped:
        print("Done")


# Gives each player a role. Returns a dict.
def role_selector():
    print(players)
    rolesList = []

    roles = {"Weerwolf": len(players) // 6,
             "Burger": 1,
             "Ziener": 1,
             "Heks": 1,
             "Jager": 1,
             "Cupido": 1,
             "Het Onschuldige Meisje": 1}
    roles["Burger"] = len(players) - roles["Weerwolf"] - (len(roles) - 2)

    # maakt een lijst met de rollen en hoe vaak ze er zijn

    for role in roles:
        for g in range((int(roles[role]))):
            rolesList.append(role)

    playerRoles = distribute_roles(players, rolesList)
    print(playerRoles)


# Distributes roles from rolesList to players
def distribute_roles(gamers, roles):
    playerNamesList = list(gamers)
    for j in range(0, len(gamers)):
        rNumber = random.randrange(len(roles))
        gamers[playerNamesList[j]] = roles[rNumber]
        del roles[rNumber]
    return gamers


async def pre_game(r):
    await r.send(
        "Het ingeslapen kakdorpje Wakkerdam wordt sinds enige tijd belaagd door weerwolven! "
        "Elke nacht veranderen bepaalde bewoners van het gehucht in mensverslindende wolven, "
        "die afschuwelijke moorden plegen... Moorden, die het daglicht niet kunnen verdragen... "
        "Wat pas nog een eeuwenoude legende was, is plotseling op onverklaarbare wijze brute "
        "realiteit geworden! Jullie dorpelingen zullen je moeten verenigen om je van deze "
        "plaag te ontdoen, en zo te zorgen, dat minstens enkelen van jullie dit griezelige avontuur"
        " overleven!")


async def permissies(r):
    override = discord.PermissionOverwrite()
    override.view_channel = True

    for e in players:
        if "Cupido" == players[e]:
            await r.channel.send(f"<@{e}> is cupido")
            cupido_channel = discord.utils.get(r.guild.text_channels, name="cupido_channel")
            cupidor = await client.fetch_user(e)
            await cupido_channel.set_permissions(cupidor, overwrite=override)

        if "Weerwolf" == players[e]:
            await r.channel.send(f"<@{e}> is weerwolv")
            weerwolf_channel = discord.utils.get(r.guild.text_channels, name="weerwolf_channel")
            weerwolf = await client.fetch_user(e)
            await weerwolf_channel.set_permissions(weerwolf, overwrite=override)

        if "Burger" == players[e]:
            await r.channel.send(f"<@{e}> is Burger")
            burger_channel = discord.utils.get(r.guild.text_channels, name="burger_channel")
            burger = await client.fetch_user(e)
            await burger_channel.set_permissions(burger, overwrite=override)

        if "Ziener" == players[e]:
            await r.channel.send(f"<@{e}> is Ziener")
            ziener_channel = discord.utils.get(r.guild.text_channels, name="ziener_channel")
            ziener = await client.fetch_user(e)
            await ziener_channel.set_permissions(ziener, overwrite=override)

        if "Heks" == players[e]:
            await r.channel.send(f"<@{e}> is Heks")
            heks_channel = discord.utils.get(r.guild.text_channels, name="heks_channel")
            heks = await client.fetch_user(e)
            await heks_channel.set_permissions(heks, overwrite=override)

        if "Jager" == players[e]:
            await r.channel.send(f"<@{e}> is Jager")
            jager_channel = discord.utils.get(r.guild.text_channels, name="jager_channel")
            jager = await client.fetch_user(e)
            await jager_channel.set_permissions(jager, overwrite=override)

        if "Het Onschuldige Meisje" == players[e]:
            await r.channel.send(f"<@{e}> is Het Onschuldige Meisje")

            meisje_channel = discord.utils.get(r.guild.text_channels, name="meisje_channel")
            meisje = await client.fetch_user(e)
            await meisje_channel.set_permissions(meisje, overwrite=override)


client.run(TOKEN)
