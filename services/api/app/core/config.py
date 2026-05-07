import os
from pathlib import Path

from dotenv import load_dotenv

# Resolve the project root so config paths work no matter where the server starts.
ROOT_DIR = Path(__file__).resolve().parents[4]

# Load local environment overrides from the project-level .env file.
load_dotenv(ROOT_DIR / ".env")

# Ollama runs as a local HTTP server by default.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# SQLite data is local-only and ignored by Git.
SQLITE_DIR = ROOT_DIR / "data" / "sqlite"
DB_PATH = SQLITE_DIR / "redstein.db"
