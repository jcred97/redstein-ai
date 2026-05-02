"use client";

import { useEffect, useState } from "react";

import { createMemory, deleteMemory, listMemories } from "@/lib/api";
import type { Memory } from "@/lib/types";

export function MemoryPanel() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [memoryTitle, setMemoryTitle] = useState("");
  const [memoryContent, setMemoryContent] = useState("");

  async function loadMemories() {
    const data = await listMemories();
    setMemories(data);
  }

  useEffect(() => {
    let isActive = true;

    listMemories()
      .then((data) => {
        if (isActive) {
          setMemories(data);
        }
      })
      .catch(() => {
        if (isActive) {
          setMemories([]);
        }
      });

    return () => {
      isActive = false;
    };
  }, []);

  async function saveMemory(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const title = memoryTitle.trim();
    const content = memoryContent.trim();

    if (!title || !content) return;

    await createMemory(title, content);
    setMemoryTitle("");
    setMemoryContent("");
    await loadMemories();
  }

  async function removeMemory(id: number) {
    await deleteMemory(id);
    await loadMemories();
  }

  return (
    <aside className="flex h-[calc(100vh-3rem)] min-h-0 flex-col rounded-lg border border-zinc-800 bg-zinc-900/70">
      <header className="shrink-0 border-b border-zinc-800 p-4">
        <h2 className="text-lg font-semibold">Memory</h2>
        <p className="mt-1 text-sm text-zinc-400">
          {memories.length} saved facts
        </p>
      </header>

      <form onSubmit={saveMemory} className="shrink-0 space-y-3 border-b border-zinc-800 p-4">
        <input
          value={memoryTitle}
          onChange={(event) => setMemoryTitle(event.target.value)}
          placeholder="Title"
          className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm text-zinc-100 outline-none focus:border-red-500"
        />
        <textarea
          value={memoryContent}
          onChange={(event) => setMemoryContent(event.target.value)}
          placeholder="Something Redstein should remember"
          className="min-h-24 w-full resize-none rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2 text-sm text-zinc-100 outline-none focus:border-red-500"
        />
        <button
          type="submit"
          className="w-full rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-500"
        >
          Save Memory
        </button>
      </form>

      <div className="min-h-0 flex-1 space-y-3 overflow-y-auto p-4">
        {memories.length === 0 ? (
          <p className="text-sm leading-6 text-zinc-400">
            No memories saved yet.
          </p>
        ) : (
          memories.map((memory) => (
            <article
              key={memory.id}
              className="rounded-lg border border-zinc-800 bg-zinc-950 p-3"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-sm font-semibold text-zinc-100">
                    {memory.title}
                  </h3>
                  <p className="mt-1 text-sm leading-6 text-zinc-300">
                    {memory.content}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => removeMemory(memory.id)}
                  className="rounded-md border border-zinc-700 px-2 py-1 text-xs text-zinc-300 hover:border-red-500 hover:text-red-300"
                >
                  Delete
                </button>
              </div>
            </article>
          ))
        )}
      </div>
    </aside>
  );
}
