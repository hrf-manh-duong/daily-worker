import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import focus_router, standup_router, tasks_router, timeline_router

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Daily Work Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(tasks_router)
app.include_router(focus_router)
app.include_router(timeline_router)
app.include_router(standup_router)
