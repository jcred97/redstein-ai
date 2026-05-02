import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[4]
DB_DIR = ROOT_DIR / "data" / "sqlite"
DB_PATH = DB_DIR / "redstein.db"


def get_connection():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
