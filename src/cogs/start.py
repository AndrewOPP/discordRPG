import discord
from discord.ext import commands
from discord import app_commands


class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(name="Menu", description="This command starts the game")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention}, ты готов к бою?")


async def setup(bot: commands.Bot):
    await bot.add_cog(Menu(bot))
