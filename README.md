# Redstein AI

Redstein AI is a local-first personal AI assistant, growing toward a second brain
for capturing and recalling useful knowledge. The current MVP provides chat and
saved memories using Next.js, FastAPI, SQLite, Ollama, and `llama3.1`.

## Current Features

- Browser chat UI in `apps/web`
- FastAPI backend in `services/api`
- Ollama chat integration
- Redstein AI identity prompt
- SQLite-backed memory storage
- Memory save, list, delete, and memory-aware replies
- SQLite-backed conversation history and recent conversation context

## Planned Next Steps

These features are planned and are not part of the current MVP:

1. Keyword search and editing for saved memories.
2. Chat answers that retrieve relevant saved entries and show their sources.
3. Richer notes, Markdown/Obsidian support, and semantic search.

Development stays incremental, with personal data stored locally by default.

## Requirements

- Python 3.14
- Node.js and npm
- Ollama with `llama3.1`

## Setup

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r services\api\requirements.txt
```

Install the local model:

```powershell
ollama pull llama3.1
```

Install frontend dependencies:

```powershell
cd apps\web
npm install
```

## Run Locally

Terminal 1, from the repo root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --app-dir services\api --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
cd apps\web
npm run dev
```

Open:

```text
http://localhost:3000
```

## Local Data

Redstein AI stores local memory in SQLite:

```text
data/sqlite/redstein.db
```

This file is created automatically when the FastAPI backend starts. It is
ignored by Git because it may contain personal user data.

Each developer or user gets their own local database.

## Useful Checks

Backend health:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
```

Frontend checks:

```powershell
cd apps\web
npm run lint
npm run build
```
