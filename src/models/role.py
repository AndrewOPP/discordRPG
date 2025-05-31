import random
from attr import dataclass
from discord import NotFound
from src.data.db import db
from src.logs import getLogger

logger = getLogger(__name__)


@dataclass
class Role:
    id: int
    name: str
    description: str
    max_hp: int
    regen_hp: int
    damage: int

    @classmethod
    async def load(cls, _id: int):
        row = await db.fetch_one("SELECT * FROM roles WHERE id = ?", (_id,), row=True)
        if row:
            logger.debug(f"Get Role: {row['name']}")
            return cls(**row)
        else:
            logger.error(f"Get Role: {_id} not found")
            raise NotFound

    @classmethod
    async def load_random(cls):
        rows = await db.fetch_all("SELECT * FROM roles", row=True)
        if rows:
            row = random.choice(rows)
            return cls(**row)
        else:
            logger.error(f"Roles table empty")
            raise NotFound
