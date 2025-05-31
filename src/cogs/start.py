from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponse
from src.ui.battle_view import StartFightView
from src.logs import getLogger
from src.models.user import User
from src.models.role import Role
from src.ui.profile_view import CreateProfileView
from src.utils import create_embed

logger = getLogger(__name__)


class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")

    @app_commands.command(name="start", description="Начни путешествие и трахни гоблинов")
    async def cmd_start(self, inter: Interaction):
        response: InteractionResponse = inter.response
        # TODO: выводить инвентарь если уже зареган, перенести в сервисы, и shop_services трахнуть
        user = await User.load(inter.user.id)

        if not user:
            embed = create_embed(
                inter.user,
                title="🏟️ Арена Гоблинов",
                description=f"`{inter.user.name.capitalize()}`, ты ступаешь на окровавленный песок перед ареной...\n"
                "Перед тобой - мертвые останки зеленых тварей, кажется кто-то хорошо потрудился.\n\n"
                "Готов стать следующим goblin-slayer?")
            await response.send_message(embed=embed, view=CreateProfileView())

        else:
            role = await Role.load(user.role)
            embed = create_embed(
                inter.user,
                title="🏟️ Арена Гоблинов",
                description=f"`{user.username}`, ты уже есть в наших рядах. Твое призвание - {role.name}!?")
            await response.send_message(embed=embed, view=StartFightView())


async def setup(bot: commands.Bot):
    await bot.add_cog(StartCog(bot))
