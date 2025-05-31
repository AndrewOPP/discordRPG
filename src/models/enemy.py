import random
from attr import dataclass
from src.logs import getLogger
from src.config import settings

logger = getLogger(__name__)


@dataclass
class Enemy:
    name: str
    lvl: int
    max_hp: int
    hp: int
    regen_hp: int
    damage: int

    @classmethod
    def generate_enemy(cls, fight_count: int):
        lvl: int = fight_count + random.choice(settings.game.enemy_lvl_random)
        damage: float = round(lvl ** random.choice(settings.game.enemy_damage_per_lvl), 1)
        hp: int = lvl * settings.game.enemy_base_hp_per_lvl
        stats = {
            "name": "Гоблин",
            "lvl": lvl,
            "max_hp": hp,
            "hp": hp,
            "regen_hp": 0,
            "damage": damage,
        }
        return cls(**stats)

    def is_alive(self):
        if self.hp > 0:
            return True

        return False
