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
game_active = False


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if "test" in message.content:
        await message.channel.send("message contains word")

@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if message.content.startswith("Monkey"):
        message.channel.send("Monkey noticed")

client.run(TOKEN)