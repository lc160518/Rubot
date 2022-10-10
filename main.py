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


running = False
joining = None
players = {}
roleNumbers = []
playerNames = []
rolesList = []
already_joined_amount = 0
i = 0
testing = False
done = None


@client.event
async def on_message(message):
    message.content = message.content.lower()

    global running

    if client.user == message.author:
        return

    if message.content.startswith("start weerwolven"):
        await startup(message)
        await cupido(message)

    if done and message.content.startswith("cupido"):
        await cupido(message)

    global created_channels

    text_channel_list = []
    if message.content.startswith("delete channels"):
        for channel in message.guild.text_channels:
            text_channel_list.append(channel)
        for channel in text_channel_list:
            if channel.name in created_channels:
                await channel.delete()


created_channels = []
possible_channels = ["main_channel", "weerwolf_channel", "burger_channel", "ziener_channel", "heks_channel",
                     "jager_channel",
                     "cupido_channel", "meisje_channel", "dood_channel"]
possible_roles = [
    "weerwolf", "burger", "ziener", "heks", "jager", "cupido", "het onschuldige meisje", "burgemeester"]
possible_integers = [0, 1, 2, 3, 4, 5, 6, 7]
created_integers = None


async def startup(s):
    global i
    global joining
    global players
    global already_joined_amount
    global done

    for e in range(0, len(possible_channels)):
        await s.guild.create_text_channel(name=possible_channels[e], reason="startup")
        created_channels.append(possible_channels[e])

    main_channel = discord.utils.get(s.guild.text_channels, name="main_channel")
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
        elif s.author in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send("<@{.author.id}> already joined".format(msg))
            already_joined_amount += 1
        if msg.author not in players and "ik" in msg.content and not testing and msg.channel == main_channel:
            players.update({msg.author: "geen rol"})

        if already_joined_amount == 3:
            await msg.channel.send("STOP MET PROBEREN, JE ZIT ER IN!!111!!")
        if msg.content.startswith("disable joining"):
            joining = False
            global playerNames
            playerNames = list(players)
            if len(players) < 6:
                await msg.channel.send("Er zijn niet genoeg spelers!")
            if len(players) >= 6:
                await msg.channel.send("Er zijn genoeg spelers, rollen worden uitgedeelt!")
            break
    role_selector()
    done = True
    print("Done")
    await pre_game(main_channel)


# Gives each player a role. Returns a dict.
def role_selector():
    global rolesList
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
        print(rNumber)
        print(gamers)
        gamers[playerNamesList[i]] = roles[rNumber]
        del roles[rNumber]
    return gamers


async def role_giver():
    print("roles given")


async def pre_game(r):
    await r.send(
        "Het ingeslapen kakdorpje Wakkerdam wordt sinds enige tijd belaagd door weerwolven! "
        "Elke nacht veranderen bepaalde bewoners van het gehucht in mensverslindende wolven, "
        "die afschuwelijke moorden plegen... Moorden, die het daglicht niet kunnen verdragen... "
        "Wat pas nog een eeuwenoude legende was, is plotseling op onverklaarbare wijze brute "
        "realiteit geworden! Jullie dorpelingen zullen je moeten verenigen om je van deze "
        "plaag te ontdoen, en zo te zorgen, dat minstens enkelen van jullie dit griezelige avontuur"
        " overleven!")


async def cupido(g):
    global done
    cupido_channel = discord.utils.get(g.guild.text_channels, name="cupido_channel")
    if done:
        await cupido_channel.send("eyo")


client.run(TOKEN)
