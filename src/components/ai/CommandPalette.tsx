"use client";

import { useEffect, useState } from "react";
import {
  FiSearch,
  FiMessageSquare,
  FiSettings,
  FiUser,
  FiPlus,
} from "react-icons/fi";

export function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setIsOpen(!isOpen);
      } else if (e.key === "Escape") {
        setIsOpen(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  if (!isOpen) return null;

  const commands = [
    {
      name: "New Chat",
      icon: <FiPlus className="text-purple-400" />,
      action: () => {
        // Handle new chat
        setIsOpen(false);
      },
    },
    {
      name: "Search Chats",
      icon: <FiSearch className="text-blue-400" />,
      action: () => {
        // Handle search
        setIsOpen(false);
      },
    },
    {
      name: "Profile Settings",
      icon: <FiUser className="text-green-400" />,
      action: () => {
        // Handle profile settings
        setIsOpen(false);
      },
    },
    {
      name: "App Settings",
      icon: <FiSettings className="text-yellow-400" />,
      action: () => {
        // Handle app settings
        setIsOpen(false);
      },
    },
  ];

  const filteredCommands = commands.filter((cmd) =>
    cmd.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-start justify-center pt-20">
      <div className="w-full max-w-xl bg-gray-800 rounded-xl overflow-hidden border border-gray-700 shadow-xl">
        <div className="relative">
          <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-gray-900 text-white px-12 py-4 focus:outline-none"
            placeholder="Type a command or search..."
            autoFocus
          />
          <kbd className="absolute right-4 top-1/2 -translate-y-1/2 bg-gray-700 text-xs px-2 py-1 rounded text-gray-300">
            ESC
          </kbd>
        </div>

        <div className="divide-y divide-gray-700 max-h-96 overflow-y-auto">
          {filteredCommands.length > 0 ? (
            filteredCommands.map((cmd) => (
              <button
                key={cmd.name}
                onClick={cmd.action}
                className="w-full px-4 py-3 text-left flex items-center gap-3 hover:bg-gray-700/50 transition-colors"
              >
                <span className="text-lg">{cmd.icon}</span>
                <span>{cmd.name}</span>
              </button>
            ))
          ) : (
            <div className="px-4 py-6 text-center text-gray-400">
              No commands found
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
