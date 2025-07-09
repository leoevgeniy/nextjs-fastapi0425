"use client";

import { useState } from "react";
import { FuturisticButton } from "../common/FuturisticButton";
import { useChat } from "@/hooks/useChat";

interface ChatInputProps {
  sessionId: string;
}

export function ChatInput({ sessionId }: ChatInputProps) {
  const [input, setInput] = useState("");
  const { append, isLoading } = useChat({ sessionId });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    append({
      role: "user",
      content: input,
      createdAt: new Date().toISOString(),
    });

    setInput("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="flex-1 bg-gray-800 bg-opacity-50 border border-purple-500 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
        placeholder="Ask your business assistant..."
        disabled={isLoading}
      />
      <FuturisticButton type="submit" disabled={!input.trim() || isLoading}>
        Send
      </FuturisticButton>
    </form>
  );
}
