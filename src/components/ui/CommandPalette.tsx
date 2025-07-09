"use client";

import { useEffect, useState, useRef } from "react";
import {
  FiSearch,
  FiMessageSquare,
  FiSettings,
  FiUser,
  FiPlus,
  FiCommand,
} from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";
import { GlassPanel } from "../common/GlassPanel";

type CommandItem = {
  id: string;
  name: string;
  icon: React.ReactNode;
  shortcut?: string;
  action: () => void;
  group: string;
};

export function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const commands: CommandItem[] = [
    {
      id: "new-chat",
      name: "New Chat",
      icon: <FiPlus className="text-purple-400" />,
      shortcut: "⌘ N",
      action: () => {
        window.location.href = "/chat";
        setIsOpen(false);
      },
      group: "General",
    },
    {
      id: "open-chats",
      name: "Open Chats",
      icon: <FiMessageSquare className="text-blue-400" />,
      shortcut: "⌘ O",
      action: () => {
        window.location.href = "/history";
        setIsOpen(false);
      },
      group: "General",
    },
    {
      id: "profile",
      name: "Profile Settings",
      icon: <FiUser className="text-green-400" />,
      action: () => {
        window.location.href = "/profile";
        setIsOpen(false);
      },
      group: "Settings",
    },
    {
      id: "settings",
      name: "Application Settings",
      icon: <FiSettings className="text-yellow-400" />,
      action: () => {
        window.location.href = "/settings";
        setIsOpen(false);
      },
      group: "Settings",
    },
  ];

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsOpen(!isOpen);
      } else if (e.key === "Escape") {
        setIsOpen(false);
      }

      // Handle arrow navigation when palette is open
      if (isOpen) {
        if (e.key === "ArrowDown") {
          e.preventDefault();
          setSelectedIndex((prev) =>
            Math.min(prev + 1, filteredCommands.length - 1)
          );
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          setSelectedIndex((prev) => Math.max(prev - 1, 0));
        } else if (e.key === "Enter" && filteredCommands[selectedIndex]) {
          e.preventDefault();
          filteredCommands[selectedIndex].action();
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, selectedIndex]);

  useEffect(() => {
    if (isOpen) {
      setQuery("");
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const filteredCommands = commands
    .filter((cmd) => cmd.name.toLowerCase().includes(query.toLowerCase()))
    .sort((a, b) => a.group.localeCompare(b.group));

  const groupedCommands = filteredCommands.reduce<
    Record<string, CommandItem[]>
  >((acc, cmd) => {
    if (!acc[cmd.group]) {
      acc[cmd.group] = [];
    }
    acc[cmd.group].push(cmd);
    return acc;
  }, {});

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          />

          <GlassPanel className="w-full max-w-xl overflow-hidden">
            <div className="relative">
              <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-transparent text-white px-12 py-4 focus:outline-none placeholder-gray-400"
                placeholder="Type a command or search..."
              />
              <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-1">
                <kbd className="bg-gray-700 text-xs px-2 py-1 rounded text-gray-300 flex items-center">
                  <FiCommand className="mr-1" /> K
                </kbd>
              </div>
            </div>

            <div className="max-h-[60vh] overflow-y-auto border-t border-gray-700/50">
              {Object.keys(groupedCommands).length > 0 ? (
                Object.entries(groupedCommands).map(([group, items]) => (
                  <div key={group}>
                    <div className="px-4 py-2 text-xs font-medium text-gray-400 uppercase tracking-wider">
                      {group}
                    </div>
                    {items.map((cmd, index) => {
                      const isSelected =
                        filteredCommands.findIndex((c) => c.id === cmd.id) ===
                        selectedIndex;
                      return (
                        <button
                          key={cmd.id}
                          onClick={cmd.action}
                          className={`w-full px-4 py-3 text-left flex items-center justify-between ${
                            isSelected
                              ? "bg-gray-700/50"
                              : "hover:bg-gray-700/30"
                          } transition-colors`}
                          onMouseEnter={() =>
                            setSelectedIndex(
                              filteredCommands.findIndex((c) => c.id === cmd.id)
                            )
                          }
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-lg">{cmd.icon}</span>
                            <span>{cmd.name}</span>
                          </div>
                          {cmd.shortcut && (
                            <kbd className="text-xs bg-gray-700 px-2 py-1 rounded text-gray-300">
                              {cmd.shortcut}
                            </kbd>
                          )}
                        </button>
                      );
                    })}
                  </div>
                ))
              ) : (
                <div className="px-4 py-6 text-center text-gray-400">
                  No commands found
                </div>
              )}
            </div>
          </GlassPanel>
        </div>
      )}
    </AnimatePresence>
  );
}
