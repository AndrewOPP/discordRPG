import discord
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ui import View, Button
from discord.ext import commands
from src.logs import getLogger

logger = getLogger(__name__)


class ShopView(View):

    def __init__(self, shop):
        super().__init__()
        self.shop = shop

    @discord.ui.button(label="купить1", style=ButtonStyle.green)
    async def clb_buy4_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

    @discord.ui.button(label="купить2", style=ButtonStyle.red)
    async def clb_buy3_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

    @discord.ui.button(label="купить3", style=ButtonStyle.gray)
    async def clb_buy2_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

    @discord.ui.button(label="купить4", style=ButtonStyle.red)
    async def clb_buy1_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

    @discord.ui.button(label="Уйти", style=ButtonStyle.green)
    async def clb_left_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")


async def setup(bot: commands.Bot):
    await bot.add_cog(ShopCog(bot))