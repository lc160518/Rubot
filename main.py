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
cupidomessage = True
zienermessage = True
ziener_done = False
weerwolven = []


@client.event
async def on_message(message):
    message.content = message.content.lower()
    global testing
    global cupidomessage

    ziener_channel = discord.utils.get(message.guild.text_channels, name="ziener_channel")

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
        cupidomessage = False
        while len(lovers) < 2:
            await cupido(message)

    if message.content.startswith("fifafofum"):
        print("a")
        ziener_done = False
        players.update({message.author.id: "Ziener"})
        players.update({398769543482179585: "Weerwolf"})
        while not ziener_done:
            print("---")
            await ziener(message)
            if not ziener_done:
                await ziener_channel.send("Dat is geen speler.")


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
    joining = True

    while joining:
        def check(m):
            return client.user != s.author \
                   and m.content == "ik" \
                   or m.content == "disable joining"

        msg = await client.wait_for("message", check=check)

        if msg.author not in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send("<@{.author.id}> joined".format(msg))
        elif msg.author in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send("<@{.author.id}> already joined".format(msg))

        if msg.author not in players and "ik" in msg.content and not testing and msg.channel == main_channel:
            players.update({msg.author.id: "geen rol"})
            spelers.append(msg.author.name.lower())

        if msg.content.startswith("disable joining"):
            joining = False
            if len(players) < 6:
                await msg.channel.send("Er zijn niet genoeg spelers!")
            if len(players) >= 6:
                await msg.channel.send("Er zijn genoeg spelers, rollen worden uitgedeelt!")
            break
    if not testing:
        role_selector()
    done = True
    print("Done")
    await pre_game(main_channel)


async def dood(victim, r):
    global players
    all_channels = ["main_channel", "weerwolf_channel", "burger_channel", "ziener_channel", "heks_channel",
                    "jager_channel", "cupido_channel", "meisje_channel", "dood_channel"]
    override = discord.PermissionOverwrite()
    override.view_channel = True
    override.send_messages = False
    players[victim] = "Dood"
    for i in range(0, len(all_channels)):
        name = all_channels[i]
        channel = discord.utils.get(r.guild.text_channels, name=name)
        victor = await client.fetch_user(victim)
        await channel.set_permissions(victor, overwrite=override)


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
    global weerwolven

    for j in range(0, len(gamers)):
        rNumber = random.randrange(len(roles))
        gamers[playerNamesList[j]] = roles[rNumber]
        del roles[rNumber]

    for i in players:
        g = await client.fetch_user(i)
        if "Weerwolf" == players[i]:
            weerwolven.append(g.name)

    return gamers


async def cupido(g):
    global lovers
    global cupidomessage
    global players

    playerIdList = list(players)

    cupido_channel = discord.utils.get(g.guild.text_channels, name="cupido_channel")
    if cupidomessage:
        await cupido_channel.send("Cupido, wie wil jij koppelen?")
        cupidomessage = False

    def check(m):
        return client.user != g.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    if msg.content.startswith("!"):
        for i in range(len(players)):
            lover = await client.fetch_user(playerIdList[i])
            if lover.name.lower() in msg.content.lower():
                if lover.name.lower() not in lovers:
                    lovers.append(lover)
                    await cupido_channel.send(f"{lover.name} is now in love")
                    print(lovers)
                else:
                    await cupido_channel.send("Narcisten zijn niet toegestaan")
    if len(lovers) == 2:
        await cupido_channel.send(f"{lovers[0].name} en {lovers[1].name} zijn nu elkaars geliefden.")
        lover1_dm = await lovers[0].create_dm()
        await lover1_dm.send(f"Jij en {lovers[1].name} zijn geliefden.")
        lover2_dm = await lovers[1].create_dm()
        await lover2_dm.send(f"Jij en {lovers[0].name} zijn geliefden.")


async def ziener(e):
    global players
    global zienermessage
    global ziener_done

    playerIdList = list(players)
    ziener_channel = discord.utils.get(e.guild.text_channels, name="ziener_channel")

    if zienermessage:
        await ziener_channel.send("Wiens identiteit wil jij ontrafelen?")
        zienermessage = False

    def check(m):
        return client.user != e.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    if msg.content.startswith("!"):
        if msg.author.name.lower() in msg.content.lower():
            await ziener_channel.send("Dat ben je zelf.")
        else:
            for i in range(len(players)):
                gepaparazzod = await client.fetch_user(playerIdList[i])
                if gepaparazzod.name.lower() in msg.content.lower():
                    await ziener_channel.send(f"{gepaparazzod.name} is {players[playerIdList[i]]}!")
                    ziener_done = True


async def weerwolf(j):
    weerwolf_channel = discord.utils.get(j.guild.text_channels, name="weerwolf_channel")

    def check(m):
        return client.user != j.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    if msg.content.startswith("!"):
        if msg.author.name.lower() in msg.content.lower():
            await weerwolf_channel.send("Zelfdoding is niet toegestaan")
        else:
            for i in weerwolven:
                y = client.fetch_user(weerwolven[i])
                if y.name.lower() in msg.content.lower():
                    await weerwolf_channel.send(f"{y.name} is gekozen")
                    await dood(weerwolven[i], j)


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
            burger_channel = discord.utils.get(r.guild.text_channels, name="burger_channel")
            burger = await client.fetch_user(e)
            await burger_channel.set_permissions(burger, overwrite=override)

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
