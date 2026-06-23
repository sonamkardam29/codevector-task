import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

pool = None

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    return pool