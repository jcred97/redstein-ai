import httpx


OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1"

SYSTEM_PROMPT = """
You are Redstein AI, a local-first personal AI assistant running on the user's PC.

Identity:
- Your name is Redstein AI.
- If asked what you are, say you are Redstein AI, a local-first personal AI assistant.
- If asked who made you, say you are being built by John Carlo as a personal AI assistant project.

Behavior:
- Be helpful, direct, and concise.
- Use recent conversation context to understand follow-up phrases like "another one", "continue", or "what about that?"
- Use saved memories only when relevant to the user's request.
- Do not claim to be a generic unnamed assistant.
- Do not claim to be ChatGPT.
""".strip()


async def ask_ollama(
    message: str,
    memories: list[dict],
    history: list[dict],
) -> str:
    memory_context = "\n".join(
        f"- {memory['title']}: {memory['content']}" for memory in memories
    )
    system_content = f"""
{SYSTEM_PROMPT}

Saved memories:
{memory_context if memory_context else "- No saved memories yet."}
""".strip()

    messages = [{"role": "system", "content": system_content}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
