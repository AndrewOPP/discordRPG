from src.data.db import db
from src.logs import getLogger

logger = getLogger(__name__)


class User:
    # TODO: Переделать под @dataclass
    def __init__(
            self, _id: int, username: str, lvl: int = 1, exp: int = 100,
            max_hp: int = 100, hp: int = 100, regen_hp: int = 0, damage: int = 2):

        self._id = _id
        self.username = username
        self.lvl = lvl
        self.exp = exp
        self.max_hp = max_hp
        self.hp = hp
        self.regen_hp = regen_hp
        self.damage = damage

    @classmethod
    async def load(cls, uid: int) -> "User":
        row = await db.fetch_one("SELECT * FROM users WHERE id = ?", (uid,), row=True)
        if row:
            logger.debug(row)
            return row
        else:
            logger.debug(f"User: {uid} not found")



