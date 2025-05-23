import discord
from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponse, Embed, Colour, ButtonStyle
from discord.ui import Button, View
from src.logs import getLogger
from src.data.model_user import User
from src.data.model_role import Role

logger = getLogger(__name__)

class StartFight(View):
    """Кнопка для создания профиль юзера, при первом запуске. Выбирает рандомно ему роль"""

    @discord.ui.button(label="В бой!", style=ButtonStyle.red)
    async def clb_profile_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        user = await User.load(inter.user.id)

        logger.debug(user.username)


class CreateProfileView(View):
    """Кнопка для создания профиль юзера, при первом запуске. Выбирает рандомно ему роль"""

    @discord.ui.button(label="Создать гладиатора", style=ButtonStyle.green)
    async def clb_profile_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response
        user = inter.user
        role = await Role.load_random()
        await User.create_user(role, user)

        embed = Embed(
            title="🏟️ Арена Гоблинов",
            description=f"`{inter.user.name.capitalize()}`, ты успешно принят в наши ряды! Наши почетные командиры, "
                        f"посоветовавшись, удостоили тебя звания '{role.name}'. Отныне твоя история такова: {role.description}"
                        f". Ступай и докажи, что ты заслуживаешь это звание!",
            colour=Colour.red())
        embed.set_author(name=f"Сосунок - {inter.user.name}", icon_url=inter.user.avatar)
        embed.set_footer(text="- Убивай или тебя будут теребить в дыру")

        await response.send_message(embed=embed, view=StartFight())


class Start(commands.Cog):
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
            embed = Embed(
                title="🏟️ Арена Гоблинов",
                description=f"`{inter.user.name.capitalize()}`, ты ступаешь на окровавленный песок перед ареной...\n"
                "Перед тобой - мертвые останки зеленых тварей, кажется кто-то хорошо потрудился.\n\n"
                "Готов стать следующим goblin-slayer?",
                colour=Colour.dark_green())
            embed.set_author(name=f"Сосунок - {inter.user.name}", icon_url=inter.user.avatar)
            embed.set_footer(text="- Убивай или тебя будут теребить в дыру")

            await response.send_message(embed=embed, view=CreateProfileView())

        else:
            role = await Role.load(user.role)
            embed = Embed(
                title="🏟️ Арена Гоблинов",
                description=f"`{user.username}`, ты уже есть в наших рядах. Твое призвание - {role.name}!?",
                colour=Colour.red())

            await response.send_message(embed=embed, view=StartFight())

async def setup(bot: commands.Bot):
    await bot.add_cog(Start(bot))
