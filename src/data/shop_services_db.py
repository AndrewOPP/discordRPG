from src.data.db import db


async def get_shop_items():
    """Получить предметы для магазина"""
    query = "SELECT * FROM items"
    params = []
    return await db.fetch_all(query, params, row=True)


async def get_user_items(user_id):
    """Получить предметы пользователя"""
    return await db.fetch_all(
        "SELECT * FROM user_items WHERE user_id = ?", (user_id,), row=True)