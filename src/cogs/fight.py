import discord
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ext import commands
from discord.ui import View, Button
from src.data.model_battle import Battle
from src.data.model_enemy import Enemy
from src.data.model_user import User
from src.logs import getLogger

logger = getLogger(__name__)


class FightView(View):
    """Кнопка для атаки/побега на поле битвы"""
    def __init__(self, battle: Battle):
        super().__init__()
        self.battle = battle

    @discord.ui.button(label="Атака", style=ButtonStyle.red)
    async def clb_attack_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response
        self.battle.player_attack()

    @discord.ui.button(label="Побег с позором", style=ButtonStyle.gray)
    async def clb_run_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response


class StartFightView(View):
    """Кнопка для создания битвы"""
    @discord.ui.button(label="В бой!", style=ButtonStyle.red)
    async def clb_profile_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        user = await User.load(inter.user.id)
        enemy = Enemy.generate_enemy()
        battle = Battle(user, enemy)
        logger.debug(f"\n{user}\n{enemy}")

        await inter.message.delete()
        await response.send_message(embed=battle.start_battle(), view=FightView(battle))


class FightCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")


async def setup(bot: commands.Bot):
    await bot.add_cog(FightCog(bot))


