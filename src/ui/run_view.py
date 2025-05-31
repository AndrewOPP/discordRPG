import discord
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ui import View, Button
from src.models.role import Role
from src.models.user import User
from src.ui.create_embeds import create_start_embed


class RunView(View):
    @discord.ui.button(label="В меню", style=ButtonStyle.gray)
    async def clb_back_to_menu_button(self, inter: Interaction, button: Button):
        from src.ui.start_view import StartFightView
        response: InteractionResponse = inter.response

        user = await User.load(inter.user.id)
        role = await Role.load(user.role)
        embed = create_start_embed(inter.user, role)
        await response.edit_message(embed=embed, view=StartFightView())
