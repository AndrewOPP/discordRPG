from random import randint
import discord
import asyncio
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ext import commands
from discord.ui import View, Button
from src.cogs.shop import ShopView
from src.data.model_battle import Battle, BattleManager
from src.data.model_inventory import SimpleInventory
from src.data.model_shop import Shop
from src.data.model_user import User
from src.data.shop_services_db import get_shop_items
from src.logs import getLogger

logger = getLogger(__name__)


class NextFightView(View):
    """Кнопка для Продолжения боя/побега на поле битвы"""
    def __init__(self, battle_manager: BattleManager):
        super().__init__()
        self.battle_manager: BattleManager = battle_manager
        self.battle: Battle = battle_manager.battle

    @discord.ui.button(label="Следующий бой!", style=ButtonStyle.red)
    async def clb_next_fight_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        await self.battle_manager.next_fight()
        await response.edit_message(embed=self.battle_manager.battle.create_embed_battle(), view=FightView(self.battle_manager))

    @discord.ui.button(label="Уйти.", style=ButtonStyle.gray)
    async def clb_quit_button(self, inter: Interaction, button: Button):
        ...


class FightView(View):
    """Кнопка для атаки/побега на поле битвы"""
    def __init__(self, battle_manager: BattleManager):
        super().__init__()
        self.battle_manager: BattleManager = battle_manager
        self.battle: Battle = battle_manager.battle

    @discord.ui.button(label="Атака", style=ButtonStyle.red)
    async def clb_attack_button(self, inter: Interaction, button: Button):
        # TODO: Чтобы реакция была только от того кто автор сообщения
        response: InteractionResponse = inter.response

        self.battle.player_attack(button)
        await response.edit_message(embed=self.battle.create_embed_battle(), view=self)
        if not self.battle.end_fight:
            progres_bar = ["▱ " for _ in range(5)]
            for i in range(len(progres_bar)):
                progres_bar[i] = "▰ "
                await inter.message.edit(embed=self.battle.create_embed_battle(progres_bar), view=self)
                await asyncio.sleep(randint(2, 6) / 10)

            self.battle.enemy_attack(button)
            await inter.message.edit(embed=self.battle.create_embed_battle(), view=self)

        if self.battle.end_fight:
            reward = self.battle.generate_fight_reward()
            end_embed = self.battle.create_embed_finish_battle(**reward)
            await self.battle.player.save_user(**reward)
            await inter.message.edit(embed=end_embed, view=NextFightView(self.battle_manager))  # TODO: новые кнопки BATTLE MANAGER

    @discord.ui.button(label="Побег с позором", style=ButtonStyle.gray)
    async def clb_run_button(self, inter: Interaction, button: Button):
        # TODO
        ...


class StartFightView(View):
    """Кнопка для создания битвы"""
    @discord.ui.button(label="В бой!", style=ButtonStyle.red)
    async def clb_profile_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        battle_manager = await BattleManager.create(inter.user.id)
        await response.edit_message(embed=battle_manager.battle.create_embed_battle(), view=FightView(battle_manager))

    @discord.ui.button(label="Магазин", style=ButtonStyle.gray)
    async def clb_shop_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response
        items = await get_shop_items()
        user = await User.load(inter.user.id)
        shop = Shop(user, items)
        await response.edit_message(embed=shop.create_embed_shop(), view=ShopView(shop))

    @discord.ui.button(label="Инвентарь", style=ButtonStyle.gray)
    async def clb_inventory_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        user = await User.load(inter.user.id)
        inventory = await SimpleInventory(user).init()
        embed = await inventory.create_embed_inventory()

        await response.edit_message(embed=embed)


class FightCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")


async def setup(bot: commands.Bot):
    await bot.add_cog(FightCog(bot))


