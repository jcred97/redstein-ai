import { ChatPanel } from "@/components/chat-panel";
import { MemoryPanel } from "@/components/memory-panel";

export default function Home() {
  return (
    <main className="h-screen overflow-hidden bg-zinc-950 text-zinc-100">
      <div className="mx-auto grid h-screen max-w-6xl gap-6 px-4 py-6 lg:grid-cols-[minmax(0,1fr)_360px]">
        <ChatPanel />
        <MemoryPanel />
      </div>
    </main>
  );
}
