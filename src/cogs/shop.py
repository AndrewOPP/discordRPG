import discord
from discord import ButtonStyle, Interaction, InteractionResponse, Embed, Colour
from discord.ui import View, Button
from discord.ext import commands
from src.logs import getLogger

logger = getLogger(__name__)


class ShopView(View):

    def __init__(self, shop):
        super().__init__()
        self.current_shop_items = shop.current_shop_items
        self.shop = shop

        for i, item in enumerate(self.current_shop_items):
            button = Button(
                label=f"Купить предмет №{i + 1}",
                style=ButtonStyle.green,
                custom_id=f"buy_item_{i}"
            )

            # Привязка обработчика с текущим значением i
            button.callback = self._make_callback(i, button)
            self.add_item(button)

            if i + 1 == 3:
                button = Button(
                    label=f"Уйти",
                    style=ButtonStyle.red,
                )
                button.callback = self._make_callback(i+1, button)
                self.add_item(button)

    def _make_callback(self, index, button):
        async def callback(interaction: Interaction):
            button.disabled = True
            item = self.current_shop_items[index]
            await self.shop.add_item_to_user(item["id"], index)
            await interaction.response.edit_message(
                embed=self.shop.create_embed_shop(),
                view=self
            )
        return callback


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")


async def setup(bot: commands.Bot):
    await bot.add_cog(ShopCog(bot))
