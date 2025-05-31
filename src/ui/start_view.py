import discord
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ui import View, Button
from src.data.crud import get_shop_items
from src.models.battle import BattleManager
from src.models.inventory import SimpleInventory
from src.models.shop import Shop
from src.models.user import User
from src.ui.battle_view import FightView
from src.ui.shop_view import ShopView


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
