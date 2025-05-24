from discord import Embed, Colour

from src.data.model_user import User


class Shop():
    def __init__(self, player: User, items):
        self.player: User = player
        self.items: list = items


    def create_embed_shop(self):
        seller_name = "Джо"
        greetings = "☄️Приветствую тебя, странник! Желаешь прикупить моих безделушек?☄️"

        embed = Embed(
            title="Прилавка Джо",
            description=greetings,
            color=Colour.yellow())

        return embed