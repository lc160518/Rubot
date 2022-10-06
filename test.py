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
ik_counter = 0
testing = False


@client.event
async def on_message(message):
    message.content = message.content.lower()

    global running

    if client.user == message.author:
        return

    # if "https://giphy.com/" or "https://tenor.com/" in message.content:
    #    await message.delete()
    if message.content.startswith("test weerwolven"):
        global testing
        global players

        players = ["Yatzil", "Flannán", "Martial", "Rana", "Ramesh", "Andrej"]
        testing = True
        await startup(message)

    if message.content.startswith("start weerwolven"):
        await startup(message)

    # deze start weervolven hier onder moet niet gebruikt worden, maar staat hier nog als voorbeeld.
    # if message.content.startswith("start Weervolven") or message.content.startswith("Start Weervolven"):
    # global main_channel
    # main_channel = client.get_channel(message.channel.id)
    # await main_channel.send("In dit channel kan er nu Weervolven worden gespeeld!")
    # await main_channel.send("Wie doet er mee met Weervolven?")

    global created_channels

    if message.content.startswith(
            "create channels") and message.author.id == 398769543482179585 or message.author.id == 627172201082388500:
        for e in range(0, len(possible_channels)):
            await message.guild.create_text_channel(name=possible_channels[e], reason="test")
            created_channels.append(possible_channels[e])
            e += 1

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

    for e in range(len(possible_channels)):
        await s.guild.create_text_channel(name=possible_channels[e], reason="test")
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

        global ik_counter

        if msg.author not in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send("<@{.author.id}> joined".format(msg))
        elif s.author in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send("<@{.author.id}> already joined".format(msg))
            already_joined_amount += 1
        if msg.author not in players and "ik" in msg.content and not testing and msg.channel == main_channel:
            players.update({msg.author: "geen rol"})
            ik_counter += 1

        if already_joined_amount == 3:
            await msg.channel.send("STOP MET PROBEREN, JE ZIT ER IN!!111!!")
            ik_counter = 6
        if msg.content.startswith("disable joining"):
            joining = False
            global playerNames
            playerNames = list(players)
            if ik_counter < 6:
                await msg.channel.send("Er zijn niet genoeg spelers!")
            if ik_counter >= 6:
                await msg.channel.send("Er zijn genoeg spelers, rollen worden uitgedeelt!")
            role_selector()


def role_selector():
    roles = {"Weerwolf": len(players) // 6,
             "Burger": 1,
             "Ziener": 1,
             "Heks": 1,
             "Jager": 1,
             "Cupido": 1,
             "Het Onschuldige Meisje": 1}
    roles["Burger"] = len(players) - roles["Weerwolf"] - (len(roles) - 2)

    # maakt een lijst met de rollen en hoe vaak ze er zijn
    global i
    i = 0
    while i != int(roles["Weerwolf"]):
        rolesList.append("Weerwolf")
        i += 1
    i = 0
    while i != int(roles["Burger"]):
        rolesList.append("Burger")
        i += 1
    i = 0
    while i != int(roles["Ziener"]):
        rolesList.append("Ziener")
        i += 1
    i = 0
    while i != int(roles["Heks"]):
        rolesList.append("Heks")
        i += 1
    i = 0
    while i != int(roles["Jager"]):
        rolesList.append("Jager")
        i += 1
    i = 0
    while i != int(roles["Cupido"]):
        rolesList.append("Cupido")
        i += 1
    i = 0
    while i != int(roles["Het Onschuldige Meisje"]):
        rolesList.append("Het Onschuldige Meisje")
        i += 1
    i = 0
    for i in range(0, len(players)):
        roleNumbers.append(i)

    for i in range(0, len(players)):
        roleNumber = random.choice(roleNumbers)
        print(roleNumber)
        roleNumbers.remove(roleNumber)
        roleReceiver = playerNames[i]
        print(roleReceiver)
        players[roleReceiver] = rolesList[roleNumber]
    print(players)


client.run(TOKEN)
