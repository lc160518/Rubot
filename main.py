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


main_channel = None
joining = None
players = {}
roleNumbers = []
playerNames = []
rolesList = []
already_joined_amount = 0
i = 0


@client.event
async def on_message(message):
    message.content = message.content.lower()
    global joining

    msg_placeholder = message

    if message.content.startswith("a"):
        await pre_game(msg_placeholder)

    if client.user == message.author:
        return
    if message.content.startswith("create channel") or message.content.startswith("Create channel"):
        await message.guild.create_text_channel(name="monkey", reason="test")

    if message.content.startswith("start Weervolven") or message.content.startswith("Start Weervolven"):
        global main_channel
        main_channel = client.get_channel(message.channel.id)
        await main_channel.send("In dit channel kan er nu Weervolven worden gespeeld!")
        await main_channel.send("Wie doet er mee met Weervolven?")

    if message.content.startswith("enable joining"):
        channel = message.channel
        global i
        i += 1
        await channel.send("Stuur \"ik\" om mee te doen!")
        joining = True

        global players

        global already_joined_amount

        while joining:
            def check(m):
                return client.user != message.author \
                       and m.content == "ik" \
                       or m.content == "disable joining" \
                       and m.channel == channel

            msg = await client.wait_for("message", check=check)

            if msg.author.name not in players and "ik" in msg.content:
                await msg.channel.send("<@{.author.id}> joined".format(msg))
            elif message.author.name in players and "ik" in msg.content:
                await msg.channel.send("<@{.author.id}> already joined".format(msg))
                already_joined_amount += 1
            if msg.author.name not in players and "ik" in msg.content:
                players.update({msg.author.name: "geen rol"})

            if already_joined_amount == 3:
                await msg.channel.send("STOP MET PROBEREN, JE ZIT ER IN!!111!!")

            if msg.content.startswith("disable joining"):
                joining = False
                global playerNames
                playerNames = list(players)
                role_selector()

        await message.channel.send("Iedereen is gejoined!")


def role_selector():
    roles = {"Weerwolf": len(players) // 6,
             "Burger": 1,
             "Ziener": 1,
             "Heks": 1,
             "Jager": 1,
             "Cupido": 1,
             "Het Onschuldige Meisje": 1}
    roles["Burger"] = len(players) - roles["Weerwolf"] - (len(roles) - 2)

    # maakt een lijst met de rollen en hoevaak ze er zijn
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
        roleNumbers.remove(roleNumber)
        roleReceiver = playerNames[i]
        players[roleReceiver] = rolesList[roleNumber]
    print(players)


async def pre_game(x):
    await x.channel.send("Het is nacht in Wakkerdam")
    await x.channel.send("Iedereen gaat slapen")
    await x.channel.send("Cupido wordt wakker en wijst twee liefjes aan")
    await x.channel.send("Nadat Cupido zijn pijl in 2 personen hun anussen heeft gestoken gaat hij blij slapen.")
    await x.channel.send(
        "De twee geliefden schrikken wakker van de pijlen in hun kontjes en kijken elkaarl iefdevol aan")
    await x.channel.send("De geliefden kruipen bij elkaar in bed en gaan lekker slapen")
    await x.channel.send("De Ziener wordt wakker na een slecht voorgevoel in de buik")
    await x.channel.send("Zo paranoïa dat ie is, loopt hij naar zijn glazen bol en ziet hij 1 iemands ware zelf")
    await x.channel.send("Na zoiets schokkends te zien valt de ziener flauw en is hij buitenbewustzijn")
    await x.channel.send("De Weerwolven worden honerig en besloten op jacht te gaan")
    await x.channel.send("Wiens kontje zullen ze opeten?")
    await x.channel.send("Na heerlijk gesmikkeld te hebben vallen ze in slaap")
    await x.channel.send("De heks wordt wakker door de stank van een aangebrand soepje.")
    await x.channel.send("Ze ziet haar levensdrankje en vergif staan.")
    await x.channel.send("Wil ze misschien 1 van die 2 gebruiken?")
    await x.channel.send("Na deze uitbundige keuze valt ze in slaap")
    await x.channel.send("Het is dag in Wakkerdam")
    await x.channel.send("Iedereen wordt wakker behalve ...")
    await x.channel.send("Na te leren dat er weerwolven zijn in de stad hebben de burgers een burgermeester nodig.")
    await x.channel.send("Wie wilt burgermeester worden?")
    await x.channel.send("Maak je speech ...")
    await x.channel.send("Stem op wie jij de burgermeester wilt hebben")
    await x.channel.send("... is de burgermeester geworden. Gefeliciteerd")
    await x.channel.send("Iemand iets sus gezien?")
    await x.channel.send("Stem iemand eruit")
    await x.channel.send("... is opgehangen en was een ...")


client.run(TOKEN)
