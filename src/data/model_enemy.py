from attr import dataclass
from src.logs import getLogger

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
    def generate_enemy(cls):
        stats = {
            "name": "Гоблин",
            "lvl": 1,
            "max_hp": 50,
            "hp": 5,
            "regen_hp": 0,
            "damage": 2,
        }
        return cls(**stats)

    def is_alive(self):
        if self.hp > 0:
            return True

        return False
