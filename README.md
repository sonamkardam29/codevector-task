# CodeVector Product API

A backend API for browsing 200,000 products with cursor-based pagination.

## Live URL
https://codevector-task.onrender.com

## Tech Stack
- Python FastAPI
- PostgreSQL (Neon)
- Deployed on Render

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| GET /products | Get paginated products (newest first) |
| GET /products?category=Electronics | Filter by category |
| GET /products?cursor=xxx | Next page |
| GET /categories | All available categories |

## How Pagination Works

Cursor-based pagination is used instead of offset pagination.

**Why?** If 50 new products are added while someone is browsing:
- ❌ Offset pagination: rows shift → user sees duplicates or misses products
- ✅ Cursor pagination: anchored to (created_at, id) → stable, no duplicates

## Example Request

GET /products?limit=20&category=Electronics&cursor=eyJjcmVhdGVkX...

## Example Response

{
  "data": [...20 products],
  "nextCursor": "eyJjcmVhdGVkX...",
  "hasMore": true,
  "count": 20
}

## Setup Locally

1. Clone the repo
2. Create virtual environment: python -m venv venv
3. Activate: venv\Scripts\activate
4. Install: pip install -r requirements.txt
5. Create .env file with DATABASE_URL
6. Run: uvicorn main:app --reload

## Seed Script

python seed.py  # Inserts 200,000 products using PostgreSQL generate_series
