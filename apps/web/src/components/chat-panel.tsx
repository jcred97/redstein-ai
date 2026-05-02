"use client";

import { useState } from "react";

import { sendChatMessage } from "@/lib/api";
import type { Message } from "@/lib/types";

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Redstein AI is ready. Ask me something.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function sendMessage(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const userMessage = input.trim();
    if (!userMessage || isLoading) return;

    const history = messages.slice(-10);

    setMessages((current) => [
      ...current,
      { role: "user", content: userMessage },
    ]);
    setInput("");
    setIsLoading(true);

    try {
      const reply = await sendChatMessage(userMessage, history);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: reply,
        },
      ]);
    } catch {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: "Could not reach the Redstein API.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="flex h-[calc(100vh-3rem)] min-h-0 flex-col">
      <header className="shrink-0 border-b border-zinc-800 pb-4">
        <h1 className="text-2xl font-semibold">Redstein AI</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Local chat powered by FastAPI, Ollama, and llama3.1
        </p>
      </header>

      <div className="min-h-0 flex-1 space-y-4 overflow-y-auto py-6">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`rounded-lg px-4 py-3 text-sm leading-6 ${
              message.role === "user"
                ? "ml-auto max-w-[80%] bg-red-600 text-white"
                : "mr-auto max-w-[80%] bg-zinc-800 text-zinc-100"
            }`}
          >
            {message.content}
          </div>
        ))}

        {isLoading && (
          <div className="mr-auto max-w-[80%] rounded-lg bg-zinc-800 px-4 py-3 text-sm text-zinc-400">
            Thinking...
          </div>
        )}
      </div>

      <form
        onSubmit={sendMessage}
        className="shrink-0 flex gap-2 border-t border-zinc-800 pt-4"
      >
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask Redstein AI..."
          className="flex-1 rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-red-500"
        />

        <button
          type="submit"
          disabled={isLoading}
          className="rounded-lg bg-red-600 px-5 py-3 text-sm font-medium text-white hover:bg-red-500 disabled:cursor-not-allowed disabled:bg-zinc-700"
        >
          Send
        </button>
      </form>
    </section>
  );
}
