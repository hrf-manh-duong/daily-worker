# Quickstart: Daily Work Tracker MVP

## Prerequisites

- Node.js 20+
- Python 3.12+
- PostgreSQL 16 running locally
- DBeaver (optional, for database inspection)

## 1) Configure environment

Create local environment files:

- `backend/.env`:
  - `DATABASE_URL=postgresql+psycopg://<user>:<password>@localhost:5432/daily_worker`
  - `APP_TIMEZONE=local`
- `frontend/.env`:
  - `VITE_API_BASE_URL=http://localhost:8000`

## 2) Start backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload --port 8000
```

## 3) Start frontend

```bash
cd frontend
npm install
npm run dev
```

Open the app in browser at the local Vite URL and verify:
- You can create tasks.
- You can start and stop focus for one task at a time.
- You can complete tasks.
- Daily timeline shows ordered activity events.

## 4) Run tests

Backend:
```bash
cd backend
source .venv/bin/activate
pytest
```

Frontend:
```bash
cd frontend
npm test
```

## 5) Rollback path (local)

When schema changes are approved and applied:

1. Create backup before migration:
   ```bash
   pg_dump -Fc -d daily_worker -f backup_before_change.dump
   ```
2. Roll back migration:
   ```bash
   cd backend
   alembic downgrade -1
   ```
3. If needed, restore backup:
   ```bash
   pg_restore -d daily_worker --clean --if-exists backup_before_change.dump
   ```
