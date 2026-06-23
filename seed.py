import asyncpg
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def seed():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    print("Seeding 200,000 products...")

    await conn.execute("""
        INSERT INTO products (name, category, price, created_at, updated_at)
        SELECT
            'Product ' || i,
            (ARRAY['Electronics','Clothing','Books','Food','Sports'])[floor(random()*5+1)],
            round((random() * 990 + 10)::numeric, 2),
            NOW() - (random() * interval '365 days'),
            NOW() - (random() * interval '30 days')
        FROM generate_series(1, 200000) AS s(i);
    """)

    print("Done! 200,000 products inserted.")
    await conn.close()

asyncio.run(seed())