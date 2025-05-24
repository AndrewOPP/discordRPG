import math
import random

from discord import Embed, Colour

from src.data.model_user import User


class Shop():
    def __init__(self, player: User, items):
        self.player: User = player
        self.items: list = items
        self.current_shop_items = self.random_three_items()


    def random_three_items(self):
        #чем больше редкость, тем меньше шанс
        weights = [max(1, 11 - item["rarity"]) for item in self.items]

        random_items = random.choices(self.items, weights=weights, k=3)

        for item in random_items:
            print(f"{item['name']} (редкость: {item['rarity']})")

        return random_items


    def create_embed_shop(self):
        greetings = "☄️Приветствую тебя, странник! Желаешь прикупить моих безделушек?☄️\n\u200b"

        embed = Embed(
            title="Прилавка Джо",
            description=greetings,
            color=Colour.yellow())

        for index, item in enumerate(self.current_shop_items):
            rarity_stars = "⭐" * math.ceil(item["rarity"] / 2)
            is_last = index == len(self.current_shop_items) - 1
            value = (
                f"\n💎Цена: {item['cost']} золота\n"
                f"💪Описание: {item['description']}"
            )
            if not is_last:
                value += "\n\u200b"

            embed.add_field(
                name=f"{item['name']} {rarity_stars}",
                value=value,
                inline=False
            )

        return embed