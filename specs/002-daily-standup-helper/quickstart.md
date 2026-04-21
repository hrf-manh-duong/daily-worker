# Quickstart — Daily Standup Helper

**Feature**: 002-daily-standup-helper

## Prerequisites

- Backend and frontend of spec 001 already run locally (see `specs/001-daily-work-tracker/quickstart.md`).
- Node.js 20, Python 3.12.

## Run

```bash
# Backend (FastAPI)
cd backend
uvicorn main:app --reload --app-dir src --port 8000

# Frontend (Vite)
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. A new "Standup" tab/panel appears next to Tasks/Focus/Timeline.

## Manual test — happy path (US1 + US2)

1. In the Tasks panel, create two tasks, complete both. Wait until tomorrow (or set
   the system clock forward) so `completed_at` falls on the previous local day.
2. Reload the app. Open the Standup panel.
3. The Yesterday textarea is pre-filled with `- Task A` / `- Task B` bullets.
4. Type "Ship the standup helper" into Today. Leave Blockers empty.
5. Click **Generate**. A Markdown preview renders with three `###` sections and
   `Blockers: None`.
6. Click **Copy**. A "Copied" toast confirms. Paste into a note app — content matches.
7. Click **Save**. The entry appears in the History list dated today.
8. Reopen tomorrow, save again for same date — it overwrites in place.

## Manual test — edge cases

- All three fields empty → **Generate** disabled.
- Paste >4000 chars into a field → API returns 422; UI shows field error.
- No tasks completed yesterday → Yesterday textarea is empty (no error).
- Non-HTTPS context → Copy falls back to textarea select-all.

## Tests to run

```bash
# Backend
cd backend && pytest tests/

# Frontend
cd frontend && npm run test
```
