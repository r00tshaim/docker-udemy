import logging
from contextlib import asynccontextmanager
from typing import Dict, Optional

import asyncpg
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client: redis.Redis = None
pg_pool: asyncpg.pool.Pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client, pg_pool
    logger.info("Connecting to Redis...")
    redis_client = redis.from_url("redis://redis:6379/0") # Use localhost for local dev, or 'redis' for docker-compose
    try:
        await redis_client.ping()
        logger.info("CONNECTED to Redis!")
    except redis.asyncio.ConnectionError as e:
        logger.error(f"ERROR connecting to Redis: {e}")
        redis_client = None

    logger.info("Connecting to PostgreSQL...")
    try:
        pg_pool = await asyncpg.create_pool("postgresql://postgres:postgres@db:5432/postgres")
        async with pg_pool.acquire() as conn:
            await conn.execute("SELECT 1")
        logger.info("CONNECTED to PostgreSQL!")
    except Exception as e:
        logger.error(f"ERROR connecting to PostgreSQL: {e}")
        pg_pool = None

    yield

    logger.info("Disconnecting from Redis...")
    if redis_client:
        await redis_client.close()
        logger.info("Disconnected from Redis.")

    logger.info("Disconnecting from PostgreSQL...")
    if pg_pool:
        await pg_pool.close()
        logger.info("Disconnected from PostgreSQL.")


app = FastAPI(title="Simple Dictionary CRUD API", lifespan=lifespan)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None

# In-memory dictionary storage
items: Dict[int, Item] = {
    1: Item(name="Item One", description="Initial item", price=10.0, tax=1.0)
}
next_id = 2

@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the local dictionary CRUD API"}

@app.get("/items")
async def list_items() -> Dict[int, Item]:
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items", status_code=201)
async def create_item(item: Item) -> dict:
    global next_id
    items[next_id] = item
    created_id = next_id
    next_id += 1
    return {"id": created_id, "item": item}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item_update: ItemUpdate) -> dict:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items[item_id]
    updated_data = item_update.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=updated_data)
    items[item_id] = updated_item
    return {"id": item_id, "item": updated_item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int) -> dict:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = items.pop(item_id)
    return {"id": item_id, "deleted": deleted}
