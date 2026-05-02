# Redstein AI

Local-first personal AI assistant MVP powered by Next.js, FastAPI, SQLite,
Ollama, and `llama3.1`.

## Current Features

- Browser chat UI in `apps/web`
- FastAPI backend in `services/api`
- Ollama chat integration
- Redstein AI identity prompt
- SQLite-backed memory storage
- Memory save, list, delete, and memory-aware replies

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
