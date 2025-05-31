from dataclasses import asdict

from attr import dataclass
from src.data.db import db
from src.logs import getLogger

logger = getLogger(__name__)


@dataclass
class User:
    id: int
    username: str
    role: int
    lvl: int
    exp: int
    coins: int
    max_hp: int
    hp: int
    regen_hp: int
    damage: int

    def __str__(self):
        return f"{self.username} (Lvl {self.lvl}) — HP: {self.hp}/{self.max_hp}, damage: {self.damage}"

    def is_alive(self):
        if self.hp > 0:
            return True

        return False

    async def save_user(self, exp: int = None, coins: int = None):
        if not exp and not coins:
            exp, coins = self.exp, self.coins
        query = "UPDATE users SET exp = exp + ?, coins = coins + ?, hp = ? WHERE id = ?"
        params = (exp, coins, self.hp, self.id)
        await db.execute_query(query, params)
        logger.debug(f"Save User: {vars(self)}")

    @classmethod
    async def load(cls, uid: int) -> "User":
        row = await db.fetch_one("SELECT * FROM users WHERE id = ?", (uid,), row=True)
        if row:
            logger.debug(f"Get User: {row['id']}")
            return cls(**row)
        else:
            logger.debug(f"Get User: {uid} not found")

    @classmethod
    async def create_user(cls, role_data, user_data):
        query = "INSERT INTO users (id, username, role, lvl, exp, max_hp, hp, regen_hp, damage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (user_data.id, user_data.name.capitalize(), role_data.id, 1, 0, role_data.max_hp, role_data.max_hp, role_data.regen_hp, role_data.damage)
        logger.debug(f"Create User: {user_data.name.capitalize()} db create")
        await db.execute_query(query, params)
