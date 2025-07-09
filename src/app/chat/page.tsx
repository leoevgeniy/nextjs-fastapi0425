"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { createNewChatSession } from "@/app/api/chat/client";

export default function ChatPage() {
  const router = useRouter();

  useEffect(() => {
    const createSession = async () => {
      const sessionId = await createNewChatSession();
      console.log(sessionId);
      router.push(`/chat/${sessionId}`);
    };
    createSession();
  }, [router]);

  return (
    <div className="flex items-center justify-center h-screen bg-gray-900">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-purple-400 mb-4">
          Creating new chat session...
        </h2>
        <div className="flex justify-center space-x-2">
          <div
            className="w-3 h-3 rounded-full bg-purple-400 animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <div
            className="w-3 h-3 rounded-full bg-blue-400 animate-bounce"
            style={{ animationDelay: "150ms" }}
          />
          <div
            className="w-3 h-3 rounded-full bg-purple-400 animate-bounce"
            style={{ animationDelay: "300ms" }}
          />
        </div>
      </div>
    </div>
  );
}
