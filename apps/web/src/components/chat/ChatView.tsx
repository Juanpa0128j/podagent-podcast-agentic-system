"use client";

export default function ChatView() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-auto p-4">
        <p className="text-slate-500">Chat messages render here.</p>
      </div>
      <div className="border-t p-4">
        <input
          type="text"
          placeholder="Ask a question..."
          className="w-full rounded border px-3 py-2"
        />
      </div>
    </div>
  );
}
