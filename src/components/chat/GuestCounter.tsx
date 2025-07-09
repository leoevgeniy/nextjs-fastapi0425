"use client";

import { useChat } from "@/hooks/useChat";

export function GuestCounter({ sessionId }: { sessionId: string }) {
  const { messages } = useChat({ sessionId, initialMessages: [] });
  const guestMessages = messages.filter((m) => m.isGuest && m.role === "user");
  const remaining = 10 - guestMessages.length;

  if (remaining <= 0 || guestMessages.length === 0) return null;

  return (
    <div className="absolute top-4 right-4 text-xs bg-gray-800/50 border border-purple-500/30 rounded-full px-3 py-1 text-purple-300 backdrop-blur-sm">
      Guest questions: {remaining} remaining
    </div>
  );
}
