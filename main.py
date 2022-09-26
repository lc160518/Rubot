# bot.py
import os
import sys
import math

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


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    print(message.content)
    if message.content.startswith("start Weervolven") or message.content.startswith("Start Weervolven"):
        print(message.content)
        main_channel = client.get_channel(message.channel.id)
        await message.channel.send("Dit channel is nu main channel!")


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if message.content.startswith("create channel") or message.content.startswith("Create channel"):
        test_channel = await message.guild.create_text_channel(name="monkey", reason="test")


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


def participants():
    players = []


client.run(TOKEN)
