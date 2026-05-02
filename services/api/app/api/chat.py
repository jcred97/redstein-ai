from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.ollama_client import ask_ollama
from app.db.session import get_connection

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = Field(default_factory=list)


@router.post("/chat")
async def chat(request: ChatRequest):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT title, content
            FROM memories
            ORDER BY created_at DESC
            LIMIT 10
            """
        ).fetchall()

    memories = [dict(row) for row in rows]
    history = [
        {"role": message.role, "content": message.content}
        for message in request.history
        if message.role in {"user", "assistant"} and message.content.strip()
    ]

    reply = await ask_ollama(
        message=request.message,
        memories=memories,
        history=history,
    )
    return {"reply": reply}
