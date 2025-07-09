"use client";

import { useEffect, useRef } from "react";
import { ChatBubble } from "./ChatBubble";
import { TypingIndicator } from "./TypingIndicator";
import { useChat } from "@/hooks/useChat";
import { Message } from "@/types/chat";
import { GlassPanel } from "../common/GlassPanel";

interface MessageStreamProps {
  sessionId: string;
  initialMessages: Message[];
}

export function MessageStream({
  sessionId,
  initialMessages,
  className = "",
}: MessageStreamProps) {
  const { messages, isTyping, append } = useChat({
    sessionId,
    initialMessages,
  });
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <GlassPanel className={"flex-1 overflow-y-auto p-4 space-y-6" + className}>
      {messages.map((message, index) => (
        <ChatBubble
          key={`${message.id}-${index}`}
          message={message}
          onEdit={(newContent) => {
            // Handle message editing
          }}
        />
      ))}
      {isTyping && <TypingIndicator />}
      <div ref={endOfMessagesRef} />
    </GlassPanel>
  );
}
