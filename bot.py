import asyncio
import discord
from discord import Message
from src.config import settings

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'START {client.user}')


@client.event
async def on_message(message: Message):
    print(message.content)


def main():
    client.run(settings.discord.token)


if __name__ == "__main__":
    asyncio.run(main())
