
# bot.py
import os

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

client.run(TOKEN)