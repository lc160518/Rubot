# bot.py
import os
import sys
import math
import time

import discord
from discord import app_commands
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


main_channel = ""
players = []
done_joining = False


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if message.content.startswith("create channel") or message.content.startswith("Create channel"):
        test_channel = await message.guild.create_text_channel(name="monkey", reason="test")

    if message.content.startswith("start Weervolven") or message.content.startswith("Start Weervolven"):
        global main_channel
        main_channel = client.get_channel(message.channel.id)
        await main_channel.send("In dit channel kan er nu Weervolven worden gespeeld!")
        await main_channel.send("Wie doet er mee met Weervolven?")

        def meedoen():
            global players
            global done_joining
            while len(players) != 24 and done_joining == False:
                for mensen in players:
                    if message.content.startswith("Ik" or "ik"):
                        players.append(message.author)
        meedoen()


def role_selector():
    roles = ["Weerwolf",
             "Burger",
             "Ziener",
             "Heks",
             "Jager",
             "Cupido",
             "Het Onschuldige meisje",
             "Burgemeester",
             "Dief"
             ]


client.run(TOKEN)
