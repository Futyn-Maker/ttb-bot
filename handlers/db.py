import asyncio

import aiosqlite
from typing import AsyncGenerator, Dict, Optional, Union

from config import DB_FILE


class Db:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        asyncio.run(self._init_db())

    async def _init_db(self) -> None:
        async with aiosqlite.connect(self.db_file) as conn:
            await conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    tg_id INTEGER NOT NULL,
                    tg_name TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    text TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)
            return await conn.commit()

    async def add_user(self, tg_id: int, tg_name: str, name: Optional[str] = None) -> Dict[str, Union[int, str]]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("INSERT INTO users (name, tg_id, tg_name) VALUES (?, ?, ?);", (name, tg_id, tg_name))
            await conn.commit()
            user_id = cursor.lastrowid
        return {"id": user_id, "name": name, "tg_id": tg_id, "tg_name": tg_name}

    async def add_response(self, user_id: int, timestamp: str, text: str) -> Dict[str, Union[int, str]]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("""
                INSERT INTO responses (user_id, timestamp, text)
                VALUES (?, ?, ?);
            """, (user_id, timestamp, text))
            await conn.commit()
            response_id = cursor.lastrowid
            return {"id": response_id, "user_id": user_id, "timestamp": timestamp, "text": text}

    async def get_user(self, tg_id: int) -> Optional[Dict[str, Union[int, str]]]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            row = await cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "tg_id": row[2],
                    "tg_name": row[3]
                }
            return None

    async def get_all_users(self) -> AsyncGenerator[Dict[str, Union[int, Optional[str]]], None]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM users;")
            async for row in cursor:
                yield {
                    "id": row[0],
                    "name": row[1],
                    "tg_id": row[2],
                    "tg_name": row[3]
                }

    async def get_user_responses(self, tg_id: int) -> AsyncGenerator[Dict[str, Union[int, str]], None]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("""
                SELECT *
                FROM responses r
                INNER JOIN users u ON r.user_id = u.id
                WHERE u.tg_id = ?;
            """, (tg_id,))
            async for row in cursor:
                yield {
                    "id": row[0],
                    "user_id": row[1],
                    "timestamp": row[2],
                    "text": row[3]
            }

    async def get_all_responses(self) -> AsyncGenerator[Dict[str, Union[int, str]], None]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM responses;")
            async for row in cursor:
                yield {
                    "id": row[0],
                    "user_id": row[1],
                    "timestamp": row[2],
                    "text": row[3]
            }
