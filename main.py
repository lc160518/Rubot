# bot.py
import os

import discord
from dotenv import load_dotenv

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
joining = True
players = []
i = 0
already_joined_amount = 0


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if message.content.startswith("create channel") or message.content.startswith("Create channel"):
        await message.guild.create_text_channel(name="monkey", reason="test")

    if message.content.startswith("a"):
        role_selector()

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

        global players
        global joining
        global already_joined_amount

        while joining:
            def check(m):
                return client.user != message.author \
                       and m.content == "ik" \
                       and m.channel == channel \
                       and m.content != "disable joining"

            msg = await client.wait_for("message", check=check)
            if message.content.startswith("disable joining"):
                await message.channel.send(message.content)
                break

            if message.author.name not in players:
                await msg.channel.send("<@{.author.id}> joined".format(msg))
            else:
                await msg.channel.send("<@{.author.id}> already joined".format(msg))
                already_joined_amount += 1
            if msg.author.name not in players:
                players.append(msg.author.name)
            print(players)

            if already_joined_amount == 3:
                await msg.channel.send("STOP MET JOINEN, JE ZIT ER IN!!111!!")

        message.channel.send("Iedereen is gejoined!")


print("monkey")


def role_selector():
    roles = {"Weerwolf": len(players) // 6,
             "Burger": 1,
             "Ziener": 1,
             "Heks": 1,
             "Jager": 1,
             "Cupido": 1,
             "Het Onschuldige Meisje": 1}
    roles["Burger"] = len(players) - roles["Weerwolf"] - (len(roles) - 2)
    rolesL = []

    global i
    i = 0
    while i != int(roles["Weerwolf"]):
        rolesL.append("Weerwolf")
        i += 1
    i = 0
    while i != int(roles["Burger"]):
        rolesL.append("Burger")
        i += 1
    i = 0
    while i != int(roles["Ziener"]):
        rolesL.append("Ziener")
        i += 1
    i = 0
    while i != int(roles["Heks"]):
        rolesL.append("Heks")
        i += 1
    i = 0
    while i != int(roles["Jager"]):
        rolesL.append("Jager")
        i += 1
    i = 0
    while i != int(roles["Cupido"]):
        rolesL.append("Cupido")
        i += 1
    i = 0
    while i != int(roles["Het Onschuldige Meisje"]):
        rolesL.append("Het Onschuldige Meisje")
        i += 1
    i = 0


client.run(TOKEN)
