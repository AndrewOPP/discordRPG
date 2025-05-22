import discord
from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponse, Embed, Colour, ButtonStyle
from discord.ui import Button, View
from src.logs import getLogger
from src.data.model_user import User

logger = getLogger(__name__)


class CreateProfileView(View):
    @discord.ui.button(label="Создать гладиатора", style=ButtonStyle.green)
    async def create_profile_button(self):
        ...


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__} is online!")

    @app_commands.command(name="start", description="Начни путешествие и трахни гоблинов")
    async def cmd_start(self, inter: Interaction):
        # TODO проверка есть ли в бд, если нету, кнопка создать гладиатора
        response: InteractionResponse = inter.response

        user = await User.load(inter.user.id)

        embed = Embed(
            title="🏟️ Арена Гоблинов",
            description=f"`{inter.user.name.capitalize()}`, ты ступаешь на окровавленный песок перед ареной...\n"
            "Перед тобой - мертвые останки зеленых тварей, кажется кто-то хорошо потрудился.\n\n"
            "Готов стать следующим goblin-slayer?",
            colour=Colour.dark_green())
        embed.set_author(name=f"Сосунок - {inter.user.name}", icon_url=inter.user.avatar)
        embed.set_footer(text="- Убивай или тебя будут теребить в дыру")

        await response.send_message(embed=embed, view=CreateProfileView())


async def setup(bot: commands.Bot):
    await bot.add_cog(Start(bot))
