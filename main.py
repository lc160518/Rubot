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
ik_counter = 1


@client.event
async def on_message(message):
    message.content = message.content.lower()
    global joining

    msg_placeholder = message

    if client.user == message.author:
        return

    if message.content.startswith("rubot stop") and message.author.id == "398769543482179585":
        await message.channel.send("eyo")
        quit()

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

            global ik_counter

            if msg.author not in players and "ik" in msg.content:
                await msg.channel.send("<@{.author.id}> joined".format(msg))
            elif message.author in players and "ik" in msg.content:
                await msg.channel.send("<@{.author.id}> already joined".format(msg))
                already_joined_amount += 1
            if msg.author not in players and "ik" in msg.content:
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

        await message.channel.send("Iedereen is gejoined!")
    global created_channels

    if message.content.startswith("create channels"):
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
possible_channels = ["weerwolf_channel", "burger_channel", "ziener_channel", "heks_channel", "jager_channel",
                     "cupido_channel", "meisje_channel", "dood_channel"]


#        weerwolfChannel
#       burgerChannel
#      zienerChannel
#     heksChannel
#    jagerChannel
#   cupidoChannel
#  meisjeChannel
# doodChannel


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
        roleNumbers.remove(roleNumber)
        roleReceiver = playerNames[i]
        players[roleReceiver] = rolesList[roleNumber]
    print(players)


client.run(TOKEN)
