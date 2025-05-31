from discord import Colour, Embed
from typing import List, Optional
from src.data.model_user import User
from src.data.db import db
from dataclasses import dataclass


class SimpleInventory:
    def __init__(self, player):
        self.player = player
        self.items = []

    async def init(self):
        self.items = await self.get_user_items()
        return self

    async def get_user_items(self):
        query = """SELECT ui.quantity, i.name, i.description FROM user_items ui JOIN items i ON ui.item_id = i.id WHERE ui.user_id = ? ORDER BY i.name ASC"""
        return await db.fetch_all(query, (self.player.id,), row=True)

    def format_items_text(self):
        if not self.items:
            return "🔒 У тебя пока нет предметов."
        items_text = []
        for item in self.items:
            items_text.append(f"• **{item['description']}** x{item['quantity']}")

        return "\n".join(items_text)

    async def create_embed_inventory(self):
        """Создать embed инвентаря"""
        embed = Embed(
            title="🧙‍♂️ Твой инвентарь",
            color=Colour.gold()
        )

        embed.add_field(
            name="📊 Характеристики",
            value=f"❤️ HP: `{self.player.hp}/{self.player.max_hp}`\n"
                  f"🗡️ Урон: `{self.player.damage}`\n"
                  f"🌟 Опыт: `{self.player.exp}`\n"
                  f"💰 Монеты: `{self.player.coins}`\n"
                  f"⬆️ Уровень: `{self.player.lvl}`",
            inline=True
        )

        items_text = self.format_items_text()
        embed.add_field(
            name="🎒 Предметы:",
            value=items_text[:1024],
            inline=False
        )

        embed.set_footer(text="Прокачивайся и стань легендой!")
        return embed

