import discord
from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponse, ButtonStyle
from discord.ui import Button, View
from src.cogs.fight import StartFightView
from src.logs import getLogger
from src.data.model_user import User
from src.data.model_role import Role
from src.utils import create_embed

logger = getLogger(__name__)


class CreateProfileView(View):
    """Кнопка для создания профиль юзера, при первом запуске. Выбирает рандомно ему роль"""

    @discord.ui.button(label="Создать гладиатора", style=ButtonStyle.green)
    async def clb_profile_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response
        user = inter.user
        role = await Role.load_random()
        await User.create_user(role, user)
        embed = create_embed(
            inter.user,
            title="🏟️ Арена Гоблинов",
            description=f"`{inter.user.name.capitalize()}`, ты успешно принят в наши ряды! Наши почетные командиры, "
                        f"посоветовавшись, удостоили тебя звания '{role.name}'.\n"
                        f"Отныне твоя история такова: {role.description}."
                        f"Ступай и докажи, что ты заслуживаешь это звание!")
        await inter.message.delete()
        await response.send_message(embed=embed, view=StartFightView())


class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")

    @app_commands.command(name="start", description="Начни путешествие и трахни гоблинов")
    async def cmd_start(self, inter: Interaction):
        response: InteractionResponse = inter.response

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
