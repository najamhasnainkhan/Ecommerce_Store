import os
import asyncpg
import asyncio
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set. Please set it before starting the backend.")

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL, max_size=5, timeout=15)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def fetch(self, query: str, *args):
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        if not self.pool:
            raise RuntimeError("Database not connected")
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

_db = Database()

async def connect_db():
    await _db.connect()

async def disconnect_db():
    await _db.disconnect()

async def fetch(query: str, *args):
    return await _db.fetch(query, *args)

async def fetchrow(query: str, *args):
    return await _db.fetchrow(query, *args)

async def execute(query: str, *args):
    return await _db.execute(query, *args)
