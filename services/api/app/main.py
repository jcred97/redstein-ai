from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.db.session import init_db

# Uvicorn loads this FastAPI instance with app.main:app.
app = FastAPI(title="Redstein AI API")

# Allow the local Next.js frontend to call the local FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep route groups in their own modules so main.py stays focused on app setup.
app.include_router(chat_router)
app.include_router(memory_router)


@app.on_event("startup")
def startup():
    # Create local SQLite tables when the backend starts.
    init_db()

@app.get("/api/health")
def health():
    # Lightweight endpoint for checking that the backend is running.
    return {"ok": True, "service": "redstein-api"}
