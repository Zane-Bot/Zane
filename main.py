import os
import datetime
import traceback
import asyncio
import asyncpg

try:
    import uvloop
except ImportError:
    print(
        """UvLoop is not installed. If you are on linux, install it with "pip install uvloop".
        If you are on windows, ignore this message.
        """)
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import discord
from discord.ext import commands

"""
This is a bot made by ir3#333.
"""


class Zane(commands.AutoShardedBot):

    def __init__(self):
        self.bot_cogs = [
            'jishaku',
            'cogs.image',
            'cogs.information'
        ]
        self.prefixes = [
            'zt.',
            'zane '
        ]
        self.color = discord.Color.blue().value
        self.init_time = datetime.datetime.utcnow()
        super().__init__(command_prefix=self.prefix)
        self.loop.create_task(self.__ainit__())

    async def __ainit__(self):
        db = await asyncpg.create_pool(
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE'],
            host=os.environ['HOST']
        )
        print("DB: Connected")
        with open("setup.sql") as f:
            await db.execute(f.read())
        print("DB: Setup.sql executed.")
        self.db = db

    @property
    def loading_emoji(self):
        return self.get_emoji(514917324709429344)

    async def prefix(self, bot, message):
        return commands.when_mentioned_or(*self.prefixes)(bot, message)

    def run(self, token: str):
        for cog in self.bot_cogs:
            try:
                self.load_extension(cog)
                print(f"Loaded: {cog}")
            except Exception:
                print(f"Error Loading {cog}: Traceback printed below.")
                traceback.print_exc()
        super().run(token)

    async def set_status(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"over {len(list(self.get_all_members()))} users | {self.prefixes[0]}help"
            )
        )

    async def on_ready(self):
        print(f"""Bot Started:

ID: {self.user.id}
UserName: {self.user.name}
Discriminator: {self.user.discriminator}
Guild Count: {len(self.guilds)}
User Count: {len(list(self.get_all_members()))}""")
        self.loop.create_task(self.set_status())
        await asyncio.sleep(120)


if __name__ == "__main__":
    Zane().run(os.environ['TOKEN'])

