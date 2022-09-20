import discord
import asyncio


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(1021842002591105065)  # channel ID goes here
        await channel.send("eyo")


client = MyClient(intents=discord.Intents.default())
client.run('ODYwMjQ0OTUzNjk0MzM5MTIy.GlFqf-.7wQ4Zhk55M8gsRjXnW_oBVkvDTRkGaVGhEb_JY')