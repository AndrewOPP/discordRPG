import math
import random
from discord import Embed, Colour
from src.data.db import db
from src.models.user import User
from src.ui.create_embeds import create_embed


class Shop:
    def __init__(self, player: User, items):
        self.player: User = player
        self.items: list = items
        self.current_shop_items = self.random_three_items()
        self.current_shop_items_bought = [[False, True], [False, True], [False, True]]
        self.coins = int(player.coins)

    def random_three_items(self):
        weights = [max(1, 11 - item["rarity"]) for item in self.items]

        random_items = random.choices(self.items, weights=weights, k=3)

        return random_items

    def coins_minus(self, amount):
        self.coins -= int(amount)

    def coins_enough_check(self, cost):
        if self.coins > cost:
            return True
        return False

    async def add_item_to_user(self, item_id: int, item_cost: int, index):
        if not self.coins_enough_check(item_cost):
            self.current_shop_items_bought[index][1] = False
            return

        query = "SELECT quantity FROM user_items WHERE user_id = ? AND item_id = ?"
        result = await db.fetch_one(query, (self.player.id, item_id))

        self.current_shop_items_bought[index][0] = True

        self.coins_minus(item_cost)

        if result:
            update_query = "UPDATE user_items SET quantity = quantity + 1 WHERE user_id = ? AND item_id = ?"
            await db.execute_query(update_query, (self.player.id, item_id))
        else:
            insert_query = "INSERT INTO user_items (user_id, item_id, quantity) VALUES (?, ?, 1)"
            await db.execute_query(insert_query, (self.player.id, item_id))

        update_query = "UPDATE users SET coins = ? WHERE id = ?"""
        await db.execute_query(update_query, (self.coins, self.player.id))

    def create_embed_shop(self):
        greetings = f"Прилавка Джо\n ☄️Приветствую тебя, странник! Желаешь прикупить моих безделушек?☄️\n\u200b"

        embed = Embed(
            title=f"💰Твой баланс: {self.coins} монет",
            description=greetings,
            color=Colour.yellow())

        for index, item in enumerate(self.current_shop_items):
            rarity_stars = "⭐" * math.ceil(item["rarity"] / 2)
            is_last = index == len(self.current_shop_items) - 1
            value = (
                f"\n💎Цена: {item['cost']} монет\n"
                f"💪Описание: {item['description']}"
            ) if self.current_shop_items_bought[index][1] else "Ты не можешь это купить, недостаточно денег"
            if not is_last:
                value += "\n\u200b"

            embed.add_field(
                name=f"{item['name']} {rarity_stars}",
                value=value if not self.current_shop_items_bought[index][0] else "КУПЛЕНО",
                inline=False
            )
        return embed

    def create_leave_embed(self, inter):
        embed = create_embed(
            inter.user,
            title="🏟️ Арена Гоблинов",
            description=f"`{self.player.username}`, ты уже есть в наших рядах. Твое призвание - {self.player.role}!?")

        return embed
