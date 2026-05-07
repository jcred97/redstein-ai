import type { Memory, Message } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function sendChatMessage(
  message: string,
  history: Message[],
): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, history }),
  });

  const data = await response.json();
  return data.reply ?? "No reply received.";
}

export async function listMemories(): Promise<Memory[]> {
  const response = await fetch(`${API_BASE_URL}/api/memory`);
  return response.json();
}

export async function createMemory(title: string, content: string): Promise<void> {
  await fetch(`${API_BASE_URL}/api/memory`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, content }),
  });
}

export async function deleteMemory(id: number): Promise<void> {
  await fetch(`${API_BASE_URL}/api/memory/${id}`, {
    method: "DELETE",
  });
}
