from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Dictionary CRUD API")

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
