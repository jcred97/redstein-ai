from fastapi import APIRouter
from pydantic import BaseModel

from app.db.session import get_connection

# All routes in this file are mounted under /api/memory.
router = APIRouter(prefix="/api/memory", tags=["memory"])


class MemoryCreate(BaseModel):
    title: str
    content: str


@router.get("")
def list_memory():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, content, created_at
            FROM memories
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


@router.post("")
def create_memory(memory: MemoryCreate):
    with get_connection() as connection:
        # Use SQL placeholders so user-provided memory text is passed safely.
        cursor = connection.execute(
            """
            INSERT INTO memories (title, content)
            VALUES (?, ?)
            """,
            (memory.title, memory.content),
        )
        connection.commit()

        # Return the created row so callers get the generated id and timestamp.
        row = connection.execute(
            """
            SELECT id, title, content, created_at
            FROM memories
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


@router.delete("/{memory_id}")
def delete_memory(memory_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )
        connection.commit()

    # rowcount is 0 when the requested memory id did not exist.
    if cursor.rowcount == 0:
        return {"ok": False, "message": "Memory not found"}

    return {"ok": True}
