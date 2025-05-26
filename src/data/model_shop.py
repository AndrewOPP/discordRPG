import math
import random

from discord import Embed, Colour

from src.data.db import db
from src.data.model_user import User


class Shop:
    #  TODO КОГДА НЕДОСТАТОЧНО ДЕНЕГ, НЕЛЬЗЯ КУПИТЬ ПРЕДМЕТ (возможно выводить в сообщение типо недостаточно денег + дизейбить кнопку.)

    def __init__(self, player: User, items):
        self.player: User = player
        self.items: list = items
        self.current_shop_items = self.random_three_items()
        self.current_shop_items_bought = [False, False, False]

    def random_three_items(self):
        #  чем больше редкость, тем меньше шанс
        weights = [max(1, 11 - item["rarity"]) for item in self.items]

        random_items = random.choices(self.items, weights=weights, k=3)

        for item in random_items:
            print(f"{item['name']} (редкость: {item['rarity']})")

        return random_items

    async def add_item_to_user(self, item_id: int, index):
        self.current_shop_items_bought[index] = True
        query = """
        SELECT quantity FROM user_items
        WHERE user_id = ? AND item_id = ?
        """
        result = await db.fetch_one(query, (self.player.id, item_id))

        if result:
            update_query = """
            UPDATE user_items
            SET quantity = quantity + 1
            WHERE user_id = ? AND item_id = ?
            """
            await db.execute_query(update_query, (self.player.id, item_id))
        else:
            insert_query = """
            INSERT INTO user_items (user_id, item_id, quantity)
            VALUES (?, ?, 1)
            """
            await db.execute_query(insert_query, (self.player.id, item_id))

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
                value=value if not self.current_shop_items_bought[index] else "КУПЛЕНО",
                inline=False
            )
        return embed
