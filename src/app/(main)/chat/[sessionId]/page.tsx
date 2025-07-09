"use client";
import { MessageStream } from "@/components/ai/MessageStream";
import { ChatInput } from "@/components/ai/ChatInput";
import { HolographicCard } from "@/components/common/HolographicCard";
import { Sidebar } from "@/components/layout/Sidebar";
import { getSessionMessages } from "@/app/api/chat/client";
import { notFound, useParams, useRouter } from "next/navigation";
import { CommandPalette } from "@/components/ui/CommandPalette";
import { Header } from "@/components/layout/Header";
import { SessionControls } from "@/components/ai/SessionControls";
import { RegistrationModal } from "@/components/auth/RegistrationModal";
import { useRegistrationModal } from "@/hooks/useRegistrationModal";
import { GuestCounter } from "@/components/chat/GuestCounter";
import { useEffect, useState } from "react";
// import { GlassPanel } from "@/components/common/GlassPanel";

export default function ChatPage() {
  const params = useParams();
  const router = useRouter();
  const [initialMessages, setInitialMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { isOpen, hideModal, guestQuestionsUsed, showModal } =
    useRegistrationModal();

  const sessionId = params.sessionId as string;
  useEffect(() => {
    const loadMessages = async () => {
      try {
        const messages = await getSessionMessages(sessionId);
        if (!messages) {
          notFound();
        }
        setInitialMessages(messages);
      } catch (error) {
        if (error.status === 429) {
          const guestMessages = initialMessages.filter(
            (m) => m.isGuest && m.role === "user"
          );
          showModal(guestMessages.length);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadMessages();
  }, [sessionId]);

  const handleRegister = () => {
    hideModal();
    router.push(
      `/register?redirect=${encodeURIComponent(window.location.pathname)}`
    );
  };

  if (isLoading) {
    return (
      <div className="flex h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center space-y-4">
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
            <p className="text-gray-400">Loading your conversation...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 overflow-hidden">
      <Sidebar currentSessionId={sessionId} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />

        <main className="flex-1 flex flex-col p-4 md:p-6 space-y-4 overflow-hidden relative">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500">
              Business AI Assistant
            </h1>
            <SessionControls sessionId={sessionId} />
          </div>

          <GuestCounter sessionId={sessionId} />

          <HolographicCard className="flex-1 flex flex-col overflow-hidden">
            <MessageStream
              sessionId={sessionId}
              initialMessages={initialMessages}
              className="flex-1 overflow-hidden"
              onLimitReached={(usedQuestions) => showModal(usedQuestions)}
            />
            <div className="p-4 border-t border-gray-700/50">
              <ChatInput
                sessionId={sessionId}
                onLimitReached={(usedQuestions) => showModal(usedQuestions)}
              />
            </div>
          </HolographicCard>
        </main>
      </div>

      <CommandPalette />

      <RegistrationModal
        isOpen={isOpen}
        onClose={hideModal}
        onRegister={handleRegister}
        guestQuestionsUsed={guestQuestionsUsed}
      />
    </div>
  );
}
