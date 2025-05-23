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
    max_hp INT,
    hp INT,
    regen_hp INT,
    damage INT,
    FOREIGN KEY (role) REFERENCES roles(id)
);
""")
