# bot.py
import os
import sys
import math
import time
import asyncio

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

q_list = [
    'Your question 1',
    'Your question 2',
    'Your question 3']

a_list = []


@client.event
async def create(message):
    submit_channel = client.fetch_channel(1021842002591105065)
    await submit_channel.send(
        "You will be asked a series of questions to create your Profile. "
        "If you accidentally typed this wait 15 seconds for it to cancel.")

    a_list = []
    channel = await message.author.create_dm()

    def check(message):
        return message.content is not None and message.channel == channel

    for question in q_list:
        await asyncio.sleep(3)
        await channel.send(question)
        message = await client.wait_for('message', check=check)
        a_list.append(message.content)

    submit_wait = True
    while submit_wait:
        await channel.send(
            'You have completed the interview, type ``submit`` to confirm')
        message = await client.wait_for('message', check=check)
        if "submit" in message.content.lower():
            submit_wait = False
            answers = "\n".join(f'{a}. {b}' for a, b in enumerate(a_list, 1))
            submit_message = f'''**Submission - Created by {message.author.mention}** \n{answers}'''
            await submit_channel.send(submit_message)


client.run(TOKEN)
