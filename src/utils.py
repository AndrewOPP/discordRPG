from discord import Embed, Colour
from discord.user import BaseUser


def create_embed(user: BaseUser, title: str, description: str):
    embed = Embed(
        title=title,
        description=description,
        colour=Colour.dark_green())
    embed.set_author(name=f"Сосунок - {user.name}", icon_url=user.avatar)
    embed.set_footer(text="- Убивай или тебя будут теребить в дыру")
    return embed
