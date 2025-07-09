"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FiMessageSquare, FiPlus, FiSettings, FiLogOut } from "react-icons/fi";
import { HolographicCard } from "../common/HolographicCard";
import { useChat } from "@/hooks/useChat";

interface SidebarProps {
  currentSessionId?: string;
}

export function Sidebar({ currentSessionId }: SidebarProps) {
  const pathname = usePathname();
  const { setMessages } = useChat({
    sessionId: currentSessionId || "",
    initialMessages: [],
  });

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="w-64 h-full flex flex-col bg-gray-900/50 border-r border-gray-800">
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500">
          AI Assistant
        </h1>
      </div>

      <div className="p-2">
        <Link
          href="/chat"
          onClick={handleNewChat}
          className="flex items-center gap-2 px-4 py-3 rounded-lg bg-purple-900/30 hover:bg-purple-900/50 text-purple-100 transition-colors"
        >
          <FiPlus className="text-purple-400" />
          <span>New Chat</span>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        <h3 className="px-4 py-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
          Recent Chats
        </h3>
        {/* Chat history items would go here */}
      </div>

      <div className="p-2 border-t border-gray-800">
        <Link
          href="/settings"
          className={`flex items-center gap-2 px-4 py-3 rounded-lg ${
            pathname === "/settings" ? "bg-gray-800/50" : "hover:bg-gray-800/30"
          } text-gray-300 transition-colors`}
        >
          <FiSettings className="text-gray-400" />
          <span>Settings</span>
        </Link>
        <button className="flex items-center gap-2 w-full px-4 py-3 rounded-lg hover:bg-gray-800/30 text-gray-300 transition-colors">
          <FiLogOut className="text-gray-400" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
}
