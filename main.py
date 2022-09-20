# bot.py
import os
import sys
import math

import discord
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} im in')


@client.event
async def on_message(message):
    print(message.content)


client.run("ODYwMjQ0OTUzNjk0MzM5MTIy.GlFqf-.7wQ4Zhk55M8gsRjXnW_oBVkvDTRkGaVGhEb_JY")
