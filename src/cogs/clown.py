from discord.ext import commands


class Clown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")


async def setup(bot):
    await bot.add_cog(Clown(bot))
