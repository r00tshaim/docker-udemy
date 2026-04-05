# FastAPI CRUD Example

A simple FastAPI project using an in-memory Python dictionary as data storage.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
source .venv/bin/activate
uv run uvicorn app.main:app --reload
```

## Endpoints

- `GET /items`
- `GET /items/{item_id}`
- `POST /items`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`
