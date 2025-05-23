import asyncio
from random import randint

from discord import Interaction, Embed, Colour

from src.data.model_enemy import Enemy
from src.data.model_user import User
from src.utils import create_embed
from src.logs import getLogger

logger = getLogger("Fight")


class Battle:
    def __init__(self, player: User, enemy):
        # TODO сделать удобный генератор embed для редактирования его постоянно
        # TODO Лог боя внизу сообщения
        # TODO Гоблин может сбежать при низком хп и будет победа
        # TODO Награды за бой от скейла уровня гоблина
        self.player: User = player
        self.enemy: Enemy = enemy
        self.turn: str = "player"
        self.round_num: int = 1
        self.last_battle_log: str = None

    def player_attack(self, button):
        # TODO Проверка живой ли гоблин и завершать битву
        button.disabled = True
        self.enemy.hp -= self.player.damage
        self.turn = "enemy"
        self.round_num += 1

        log_text = f"Лог: 👤 Ваш удар по гоблину на {self.player.damage} урона"
        logger.debug(f"{log_text} Здоровье гоблина: {self.enemy.hp}/{self.enemy.max_hp}")
        self.last_battle_log = log_text

    def enemy_attack(self, button):
        button.disabled = False

        self.player.hp -= self.enemy.damage
        self.turn = "player"
        self.round_num += 1

        log_text = f"Лог: 👹 Удар гоблина по вам на {self.enemy.damage} урона"
        logger.debug(f"{log_text} Здоровье игрока: {self.player.hp}/{self.player.max_hp}")
        self.last_battle_log = log_text

    def create_embed_battle(self, progress_bar=None) -> Embed:
        start_title = f"⚔️ Битва началась! Твой ход! Раунд {self.round_num}"
        start_footer = "Используй кнопки ниже для атаки или защиты."
        turn = "Бейся! Ваш ход!" if self.turn == "player" else "Ходит гоблин!"
        title = f"⚔️ {turn} Раунд {self.round_num}"
        color = Colour.dark_green() if self.turn == "player" else Colour.dark_red()

        embed = Embed(
            title=start_title if not self.last_battle_log else title,
            description=None if not progress_bar else "".join(progress_bar),
            color=color)

        embed.add_field(
            name=f"`👤` Игрок: {self.player.username}| lvl: {self.player.lvl}",
            value=(
                f"**HP:** {self.player.hp}/{self.player.max_hp}\n"
                f"**Урон:** {self.player.damage}"),
            inline=False)

        embed.add_field(
            name=f"`👹` Враг: {self.enemy.name} | lvl: {self.enemy.lvl}",
            value=(
                f"**HP:** {self.enemy.hp}/{self.enemy.max_hp}\n"
                f"**Урон:** {self.enemy.damage}"),
            inline=False)

        embed.set_footer(text=self.last_battle_log if self.last_battle_log else start_footer)
        return embed
