import aiosqlite as sql
from typing import Union, Tuple, List
from src.logs import getLogger

getLogger("aiosqlite").setLevel("WARNING")


class Database:
    def __init__(self):
        self.db_path = "src/data/database.db"

    async def _connect(self):
        return sql.connect(self.db_path)

    async def execute_query(self, query: str, params: Union[Tuple, List] = ()) -> None:
        """Выполняет запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        async with await self._connect() as con:
            async with con.cursor() as cur:
                await cur.execute(query, params)
            await con.commit()

    async def fetch_all(self, query: str, params: Union[Tuple, List] = (), row: bool = False) -> List[Tuple]:
        """Выполняет SELECT запрос и возвращает записи"""
        async with await self._connect() as con:
            if row:
                con.row_factory = sql.Row
            async with con.cursor() as cur:
                await cur.execute(query, params)
                return await cur.fetchall()

    async def fetch_one(self, query: str, params: Union[Tuple, List] = (), row: bool = False) -> List[Tuple]:
        """Выполняет SELECT запрос и возвращает записи"""
        async with await self._connect() as con:
            if row:
                con.row_factory = sql.Row
            async with con.cursor() as cur:
                await cur.execute(query, params)
                return await cur.fetchone()


db = Database()


async def init_db():
    await db.execute_query("""
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT, 
    max_hp INT,
    regen_hp INT,
    damage INT
);    
""")

    await db.execute_query("""
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    role INT,
    lvl INT,
    exp INT,
    coins INT DEFAULT 0,
    max_hp INT,
    hp INT,
    regen_hp INT,
    damage INT,
    FOREIGN KEY (role) REFERENCES roles(id)
);
""")

    await db.execute_query("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    bonus_damage INT DEFAULT 0,
    bonus_hp INT DEFAULT 0,
    cost INT DEFAULT 0,
    rarity INT CHECK(rarity BETWEEN 1 AND 10)
);
    """)

    await db.execute_query("""
CREATE TABLE IF NOT EXISTS user_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id BIGINT,
    item_id INTEGER,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);
    """)

#     await db.execute_query("""
# INSERT OR IGNORE INTO items (name, description, bonus_damage, bonus_hp, cost, rarity) VALUES
# ('Wooden Sword', 'Простой деревянный меч. +2 урона.', 2, 0, 10, 1),
# ('Leather Armor', 'Кожаная броня. +5 HP.', 0, 5, 15, 2),
# ('Iron Axe', 'Тяжёлый топор. +5 урона.', 5, 0, 40, 3),
# ('Steel Shield', 'Стальной щит. +15 HP.', 0, 15, 60, 4),
# ('Fire Dagger', 'Огненный кинжал. +8 урона.', 8, 0, 85, 5),
# ('Amulet of Life', 'Амулет жизни. +5 урона, +10 HP.', 5, 10, 120, 6),
# ('Dark Blade', 'Клинок Тьмы. +15 урона.', 15, 0, 180, 7),
# ('Dragon Scale Armor', 'Броня из чешуи дракона. +30 HP.', 0, 30, 250, 8),
# ('Storm Hammer', 'Молот Шторма. +12 урона, +10 HP.', 12, 10, 300, 9),
# ('Celestial Crown', 'Небесная корона. +20 урона, +25 HP.', 20, 25, 500, 10)
#   """)
