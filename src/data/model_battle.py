from discord import Interaction, Embed, Colour
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
        self.player = player
        self.enemy = enemy
        self.turn = "player"
        self.round_num = 1

    def player_attack(self):
        # TODO Проверка живой ли гоблин и завершать битву
        self.enemy.hp -= self.player.damage
        logger.debug(f"Удар по гоблину на {self.player.damage} урона. Здоровье гоблина: {self.enemy.hp}/{self.enemy.max_hp}")

    def start_battle(self) -> Embed:
        embed = Embed(
            title=f"⚔️ Битва началась! Раунд {self.round_num}",
            color=Colour.dark_green())

        embed.add_field(
            name=f"👤 Игрок: {self.player.username}| lvl: {self.player.lvl}",
            value=(
                f"**HP:** {self.player.hp}/{self.player.max_hp}\n"
                f"**Урон:** {self.player.damage}"),
            inline=True)

        embed.add_field(
            name=f"👹 Враг: {self.enemy.name} | lvl: {self.enemy.lvl}",
            value=(
                f"**HP:** {self.enemy.hp}/{self.enemy.max_hp}\n"
                f"**Урон:** {self.enemy.damage}"),
            inline=True)

        embed.set_footer(text="Используй кнопки ниже для атаки или защиты.")
        return embed
