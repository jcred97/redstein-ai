from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.ollama_client import ask_ollama
from app.db.conversation_store import (
    get_default_conversation_id,
    list_recent_messages,
    save_message,
)
from app.db.session import get_connection

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    # Use a new empty list per request when the frontend does not send history.
    history: list[ChatMessage] = Field(default_factory=list)


@router.post("/chat")
async def chat(request: ChatRequest):
    with get_connection() as connection:
        conversation_id = get_default_conversation_id(connection)

        # Keep prompt context small by sending only the newest saved memories.
        rows = connection.execute(
            """
            SELECT title, content
            FROM memories
            ORDER BY created_at DESC
            LIMIT 10
            """
        ).fetchall()

    memories = [dict(row) for row in rows]

    # Keep only valid chat roles and non-empty messages before sending to Ollama.
    history = [
        {"role": message.role, "content": message.content}
        for message in request.history
        if message.role in {"user", "assistant"} and message.content.strip()
    ]

    # If the browser has no history, fall back to the persisted local conversation.
    if not history:
        with get_connection() as connection:
            history = list_recent_messages(connection, conversation_id)

    # Persist both sides of the exchange so future chats can recover context.
    with get_connection() as connection:
        save_message(connection, conversation_id, "user", request.message)

    reply = await ask_ollama(
        message=request.message,
        memories=memories,
        history=history,
    )

    with get_connection() as connection:
        save_message(connection, conversation_id, "assistant", reply)

    return {"reply": reply}
