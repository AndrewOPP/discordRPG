
from attr import dataclass
from src.data.db import db
from src.logs import getLogger
from discord import NotFound

logger = getLogger(__name__)


@dataclass
class User:
    id: int
    username: str
    role: int
    lvl: int
    exp: int
    max_hp: int
    hp: int
    regen_hp: int
    damage: int

    @classmethod
    async def load(cls, uid: int) -> "User":
        row = await db.fetch_one("SELECT * FROM users WHERE id = ?", (uid,), row=True)
        if row:
            logger.debug(row)
            return cls(**row)
        else:
            logger.debug(f"User: {uid} not found")

    @classmethod
    async def create_user(cls, role_data, user_data):
        query = "INSERT INTO users (id, username, role, lvl, exp, max_hp, hp, regen_hp, damage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (user_data.id, user_data.name.capitalize(), role_data.id, 1, 0, role_data.max_hp, 50, role_data.regen_hp, role_data.damage)
        logger.debug(f"User: {user_data.name.capitalize()} успешно зареган")
        await db.execute_query(query, params)
