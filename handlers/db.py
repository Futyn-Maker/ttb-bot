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
                    tg_name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    workplace TEXT,
                    workload INTEGER,
                    subjects TEXT,
                    teaching_experience INTEGER,
                    class_management BOOLEAN,
                    classes TEXT,
                    source TEXT,
                    consent_study BOOLEAN,
                    consent_personal_data BOOLEAN,
                    notifications_wanted BOOLEAN
                );

                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    timestamp_start TEXT NOT NULL,
                    timestamp_end TEXT,
                    text TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)
            await conn.commit()


    async def add_user(self, tg_id: int, tg_name: str, name: Optional[str] = None, notifications_wanted: bool = True, **kwargs) -> Dict[str, Union[int, str, Optional[bool]]]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("""
                INSERT INTO users (name, tg_id, tg_name, age, gender, workplace, workload, subjects, teaching_experience, class_management, classes, source, consent_study, consent_personal_data, notifications_wanted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (name, tg_id, tg_name, kwargs.get("age"), kwargs.get("gender"), kwargs.get("workplace"), kwargs.get("workload"), kwargs.get("subjects"), kwargs.get("teaching_experience"), kwargs.get("class_management"), kwargs.get("classes"), kwargs.get("source"), kwargs.get("consent_study"), kwargs.get("consent_personal_data"), notifications_wanted))
            await conn.commit()
            user_id = cursor.lastrowid
            return {"id": user_id, "name": name, "tg_id": tg_id, "tg_name": tg_name, "notifications_wanted": notifications_wanted, **kwargs}


    async def update_notifications_wanted(self, user_id: int, notifications_wanted: bool) -> None:
        async with aiosqlite.connect(self.db_file) as conn:
            await conn.execute("""
                UPDATE users SET notifications_wanted = ? WHERE id = ?;
            """, (notifications_wanted, user_id))
            await conn.commit()


    async def add_response(self, user_id: int, timestamp_start: str, timestamp_end: str, text: str) -> Dict[str, Union[int, str]]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("""
                INSERT INTO responses (user_id, timestamp_start, timestamp_end, text)
                VALUES (?, ?, ?, ?);
            """, (user_id, timestamp_start, timestamp_end, text))
            await conn.commit()
            response_id = cursor.lastrowid
            return {"id": response_id, "user_id": user_id, "timestamp_start": timestamp_start, "timestamp_end": timestamp_end, "text": text}


    async def get_user(self, id: int, id_type: str = "tg_id") -> Optional[Dict[str, Union[int, str, Optional[bool]]]]:
        async with aiosqlite.connect(self.db_file) as conn:
            query = "SELECT * FROM users WHERE {} = ?;".format(id_type)
            cursor = await conn.execute(query, (id,))
            row = await cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "tg_id": row[2],
                    "tg_name": row[3],
                    "notifications_wanted": row[-1],
                    "age": row[4],
                    "gender": row[5],
                    "workplace": row[6],
                    "workload": row[7],
                    "subjects": row[8],
                    "teaching_experience": row[9],
                    "class_management": row[10],
                    "classes": row[11],
                    "source": row[12],
                    "consent_study": row[13],
                    "consent_personal_data": row[14]
                }
            return None


    async def get_all_users(self) -> AsyncGenerator[Dict[str, Union[int, str, Optional[bool]]], None]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM users;")
            async for row in cursor:
                yield {
                    "id": row[0],
                    "name": row[1],
                    "tg_id": row[2],
                    "tg_name": row[3],
                    "notifications_wanted": row[-1],
                    "age": row[4],
                    "gender": row[5],
                    "workplace": row[6],
                    "workload": row[7],
                    "subjects": row[8],
                    "teaching_experience": row[9],
                    "class_management": row[10],
                    "classes": row[11],
                    "source": row[12],
                    "consent_study": row[13],
                    "consent_personal_data": row[14]
                }


    async def get_user_responses(self, user_id: int) -> AsyncGenerator[Dict[str, Union[int, str]], None]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("""
                SELECT *
                FROM responses
                WHERE user_id = ?
                ORDER BY datetime(timestamp_start);
            """, (user_id,))
            async for row in cursor:
                yield {
                    "id": row[0],
                    "user_id": row[1],
                    "timestamp_start": row[2],
                    "timestamp_end": row[3],
                    "text": row[4]
            }


    async def get_all_responses(self) -> AsyncGenerator[Dict[str, Union[int, str]], None]:
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM responses ORDER BY datetime(timestamp_start);")
            async for row in cursor:
                yield {
                    "id": row[0],
                    "user_id": row[1],
                    "timestamp_start": row[2],
                    "timestamp_end": row[3],
                    "text": row[4]
            }
