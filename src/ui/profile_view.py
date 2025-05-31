import discord
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ui import View, Button
from src.ui.battle_view import StartFightView
from src.models.role import Role
from src.models.user import User
from src.utils import create_embed


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
        await response.edit_message(embed=embed, view=StartFightView())
