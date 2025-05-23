import asyncio
import discord
import os
from src.config import settings
from src.logs import getLogger
from src.data.db import init_db
from discord.ext import commands

getLogger("discord.client").setLevel("WARNING")
getLogger("discord.gateway").setLevel("WARNING")
getLogger("discord.http").setLevel("WARNING")
getLogger("discord.webhook").setLevel("WARNING")

logger = getLogger(__name__)


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} Start')
    await bot.tree.sync()


async def load_commands():
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"src.cogs.{filename[:-3]}")


async def main():
    await init_db()
    await load_commands()
    await bot.start(settings.discord.token)

if __name__ == "__main__":
    asyncio.run(main())
