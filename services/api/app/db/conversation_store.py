import sqlite3

# Phase 1 uses one conversation until the UI supports multiple chat threads.
DEFAULT_CONVERSATION_TITLE = "Default"


def get_default_conversation_id(connection: sqlite3.Connection) -> int:
    # Use a parameterized query so the title is passed safely into SQL.
    row = connection.execute(
        """
        SELECT id
        FROM conversations
        WHERE title = ?
        ORDER BY id
        LIMIT 1
        """,
        (DEFAULT_CONVERSATION_TITLE,),
    ).fetchone()

    if row:
        return int(row["id"])

    # Create the default conversation on first use.
    cursor = connection.execute(
        """
        INSERT INTO conversations (title)
        VALUES (?)
        """,
        (DEFAULT_CONVERSATION_TITLE,),
    )
    connection.commit()
    return int(cursor.lastrowid)


def list_recent_messages(
    connection: sqlite3.Connection,
    conversation_id: int,
    limit: int = 10,
) -> list[dict]:
    rows = connection.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (conversation_id, limit),
    ).fetchall()

    # SQL fetches newest first; Ollama chat history should read oldest to newest.
    return [dict(row) for row in reversed(rows)]


def save_message(
    connection: sqlite3.Connection,
    conversation_id: int,
    role: str,
    content: str,
) -> None:
    connection.execute(
        """
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
        """,
        (conversation_id, role, content),
    )

    # Keep the parent conversation sortable by recent activity.
    connection.execute(
        """
        UPDATE conversations
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (conversation_id,),
    )
    connection.commit()
