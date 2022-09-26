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
async def get_channel():
    channel = client.get_channel(1021842002591105065)
    await channel.send("eyo")

@client.event
async def on_message(message):
    main_channel = message.channel.id

client.run(TOKEN)
