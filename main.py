from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from database import get_pool
import base64
import json
from typing import Optional

app = FastAPI(title="CodeVector Product API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def encode_cursor(created_at, product_id):
    data = {"created_at": str(created_at), "id": str(product_id)}
    return base64.b64encode(json.dumps(data).encode()).decode()

def decode_cursor(cursor: str):
    data = json.loads(base64.b64decode(cursor).decode())
    return data["created_at"], data["id"]

@app.get("/")
async def root():
    return {"message": "CodeVector Product API is running!"}

@app.get("/products")
async def get_products(
    limit: int = Query(default=20, ge=1, le=100),
    cursor: Optional[str] = None,
    category: Optional[str] = None
):
    pool = await get_pool()

    conditions = []
    params = []
    param_count = 1

    if cursor:
        try:
            created_at, product_id = decode_cursor(cursor)
            conditions.append(
                f"(created_at, id) < (${param_count}::timestamptz, ${param_count+1}::uuid)"
            )
            params.extend([created_at, product_id])
            param_count += 2
        except:
            pass

    if category:
        conditions.append(f"category = ${param_count}")
        params.append(category)
        param_count += 1

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT id, name, category, price, created_at, updated_at
        FROM products
        {where_clause}
        ORDER BY created_at DESC, id DESC
        LIMIT {limit + 1}
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    results = [dict(row) for row in rows]

    has_more = len(results) > limit
    items = results[:limit]

    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = encode_cursor(last["created_at"], last["id"])

    for item in items:
        item["created_at"] = item["created_at"].isoformat()
        item["updated_at"] = item["updated_at"].isoformat()
        item["price"] = float(item["price"])

    return {
        "data": items,
        "nextCursor": next_cursor,
        "hasMore": has_more,
        "count": len(items)
    }

@app.get("/categories")
async def get_categories():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT DISTINCT category FROM products ORDER BY category"
        )
    return {"categories": [row["category"] for row in rows]}