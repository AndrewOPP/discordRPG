import sqlite3 as sql
from typing import Union, Tuple, List


class Database:
    def __init__(self):
        self.db_path = "src/data/database.db"

    def _connect(self):
        return sql.connect(self.db_path)

    def execute_query(self, query: str, params: Union[Tuple, List] = ()) -> None:
        """Выполняет запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        with self._connect() as con:
            cursor = con.cursor()
            cursor.execute(query, params)
            con.commit()

    def fetch_all(self, query: str, params: Union[Tuple, List] = (), row: bool = False) -> List[Tuple]:
        """Выполняет SELECT запрос и возвращает записи"""
        with self._connect() as con:
            if row:
                con.row_factory = sql.Row
            cursor = con.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Union[Tuple, List] = (), row: bool = False) -> List[Tuple]:
        """Выполняет SELECT запрос и возвращает записи"""
        with self._connect() as con:
            if row:
                con.row_factory = sql.Row
            cursor = con.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()


db = Database()


def init_db():
    db.execute_query("""
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    lvl INT,
    xp INT,
    max_hp INT,
    regen_hp INT,
    damage INT,
    battle_round INT
);
""")
