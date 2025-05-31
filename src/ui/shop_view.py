from discord import ButtonStyle, Interaction
from discord.ui import View, Button


class ShopView(View):

    def __init__(self, shop):
        super().__init__()
        self.current_shop_items = shop.current_shop_items
        self.shop = shop

        for i, item in enumerate(self.current_shop_items):
            button = Button(
                label=f"Купить предмет №{i + 1}",
                style=ButtonStyle.green,
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
            if button.label == "Уйти":
                from src.ui.start_view import StartFightView
                embed = self.shop.create_leave_embed(interaction)
                await interaction.response.edit_message(embed=embed, view=StartFightView())
            else:
                button.disabled = True
                item = self.current_shop_items[index]
                await self.shop.add_item_to_user(item["id"], item["cost"], index)
                await interaction.response.edit_message(
                    embed=self.shop.create_embed_shop(),
                    view=self)

        return callback
