from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponse, Embed
from src.logs import getLogger

logger = getLogger(__name__)


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online!")

    @app_commands.command(name="start", description="Начни путешествие и трахни гоблинов")
    async def cmd_start(self, inter: Interaction):
        response: InteractionResponse = inter.response

        embed = Embed(
            title="🏟️ Арена Гоблинов",
            description=f"`{inter.user.name.capitalize()}`, ты ступаешь на окровавленный песок перед ареной...\n"
            "Перед тобой - мертвые останки зеленых тварей, кажется кто-то хорошо потрудился.\n\n"
            "Готов стать следующим goblin-slayer?")
        embed.set_author(name=f"Сосунок - {inter.user.name}", icon_url=inter.user.avatar)
        embed.set_footer(text="- Убивай или тебя будут теребить в дыру")

        await response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Start(bot))
