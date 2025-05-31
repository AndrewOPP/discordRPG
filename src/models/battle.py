from discord import Embed, Colour
from src.models.enemy import Enemy
from src.models.user import User
from src.logs import getLogger
from src.config import settings

logger = getLogger("Fight")


class Battle:
    def __init__(self, player: User, enemy: Enemy):
        # TODO Гоблин может сбежать при низком хп и будет победа
        self.player: User = player
        self.enemy: Enemy = enemy
        self.turn: str = "player"
        self.round_num: int = 1
        self.last_battle_log: str = None
        self.end_fight = False

    def generate_fight_reward(self) -> dict:
        return {
            "exp": int(settings.game.exp_reward_base * (self.enemy.lvl * settings.game.exp_coef_reward)),
            "coins": int(settings.game.coin_reward_base * (self.enemy.lvl * settings.game.coins_coef_reward_per_lvl))
        }

    def finish_the_fight(self):
        if self.turn == "player":
            log_text = f"Лог: 👤 Ваш удар сокрушает гоблина!"
            logger.debug(f"{log_text} Здоровье гоблина: {self.enemy.hp}/{self.enemy.max_hp}")

        else:
            log_text = f"Лог: 👹 Удар гоблина размазал вас по стенке!"
            logger.debug(f"{log_text} Здоровье игрока: {self.player.hp}/{self.player.max_hp}")

        self.last_battle_log = log_text
        self.end_fight = True

    def player_attack(self, button):
        button.disabled = True
        self.enemy.hp -= self.player.damage
        if self.enemy.is_alive():
            self.turn = "enemy"
            self.round_num += 1

            log_text = f"Лог: 👤 Ваш удар по гоблину на {self.player.damage} урона"
            logger.debug(f"{log_text} Здоровье гоблина: {self.enemy.hp}/{self.enemy.max_hp}")
            self.last_battle_log = log_text
            return

        self.finish_the_fight()

    def enemy_attack(self, button):
        button.disabled = False
        self.player.hp -= self.enemy.damage
        if self.player.is_alive():
            self.turn = "player"
            self.round_num += 1

            log_text = f"Лог: 👹 Удар гоблина по вам на {self.enemy.damage} урона"
            logger.debug(f"{log_text} Здоровье игрока: {self.player.hp}/{self.player.max_hp}")
            self.last_battle_log = log_text
            return

        self.finish_the_fight()

    def create_embed_finish_battle(self, exp: int, coins: int) -> Embed:
        if self.turn == "player":
            embed = Embed(
                title="🏁 Битва завершена!",
                description=f"`👤` **Игрок: {self.player.username}** поверг **{self.enemy.name}** на {self.round_num} раунде!",
                color=Colour.dark_green())
            embed.add_field(name="`💖` Оставшееся HP", value=f"{self.player.hp}/{self.player.max_hp}")
            embed.add_field(name="`✨` Получено опыта", value=f"{exp} XP")
            embed.add_field(name="`💰` Получено золота", value=f"{coins} монет")
            embed.set_footer(text=self.last_battle_log)
            return embed
        else:
            embed = Embed(
                title="🏁 Битва завершена!",
                description=f"`👹` **Противник: {self.enemy.name}** избил **{self.player.username}** на {self.round_num} раунде!\n"
                            "Позор... может в следующий раз хотя бы укусишь в ответ?\n\n"
                            "В следующий раз будешь тренироваться на тараканах, челядь...",
                color=Colour.dark_red())
            embed.add_field(name="`💖` Оставшееся HP противника", value=f"{self.enemy.hp}/{self.enemy.max_hp}")
            embed.set_footer(text=self.last_battle_log)
            return embed

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


class BattleManager:
    def __init__(self, player: User):
        self.player: User = player
        self.battle: Battle = None
        self.fight_count: int = 1

    @classmethod
    async def create(cls, user_id) -> "BattleManager":
        player = await User.load(user_id)
        manager = cls(player)
        await manager.create_fight()
        return manager

    async def create_fight(self) -> "Battle":
        user = await User.load(self.player.id)
        enemy = Enemy.generate_enemy(self.fight_count)
        self.battle = Battle(user, enemy)
        return self.battle

    async def next_fight(self) -> "Battle":
        self.fight_count += 1
        return await self.create_fight()

