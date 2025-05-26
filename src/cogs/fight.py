from random import randint
import discord
import asyncio
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ext import commands
from discord.ui import View, Button

from src.cogs.shop import ShopView
from src.data.model_battle import Battle
from src.data.model_enemy import Enemy
from src.data.model_shop import Shop
from src.data.model_user import User
from src.data.shop_services_db import get_shop_items
from src.logs import getLogger

logger = getLogger(__name__)


class FightView(View):
    """Кнопка для атаки/побега на поле битвы"""
    def __init__(self, battle: Battle):
        super().__init__()
        self.battle = battle

    @discord.ui.button(label="Атака", style=ButtonStyle.red)
    async def clb_attack_button(self, inter: Interaction, button: Button):
        # TODO: Чтобы реакция была только от того кто автор сообщения
        response: InteractionResponse = inter.response

        self.battle.player_attack(button)
        await response.edit_message(embed=self.battle.create_embed_battle(), view=self)

        progres_bar = ["▱ " for _ in range(5)]
        for i in range(len(progres_bar)):
            progres_bar[i] = "▰ "
            await inter.message.edit(embed=self.battle.create_embed_battle(progres_bar), view=self)
            await asyncio.sleep(randint(2, 6) / 10)

        self.battle.enemy_attack(button)
        await inter.message.edit(embed=self.battle.create_embed_battle(), view=self)

        reward = self.battle.generate_fight_reward()
        end_embed = self.battle.create_embed_finish_battle(**reward)
        await self.battle.player.save_user(**reward)
        await inter.message.edit(embed=end_embed, view=None)  # TODO: новые кнопки

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
        await response.edit_message(embed=battle.create_embed_battle(), view=FightView(battle))

    @discord.ui.button(label="Магазин", style=ButtonStyle.gray)
    async def clb_shop_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response
        items = await get_shop_items()
        user = await User.load(inter.user.id)
        shop = Shop(user, items)
        await response.edit_message(embed=shop.create_embed_shop(), view=ShopView(shop))


class FightCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")


async def setup(bot: commands.Bot):
    await bot.add_cog(FightCog(bot))


