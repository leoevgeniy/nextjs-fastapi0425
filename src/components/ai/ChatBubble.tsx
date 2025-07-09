"use client";

import { useState } from "react";
import { FiEdit2, FiCopy, FiCheck } from "react-icons/fi";
import { Message } from "@/types/chat";
import { GlassPanel } from "../common/GlassPanel";

interface ChatBubbleProps {
  message: Message;
  onEdit?: (content: string) => void;
}

export function ChatBubble({ message, onEdit }: ChatBubbleProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(message.content);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSaveEdit = () => {
    onEdit?.(editedContent);
    setIsEditing(false);
  };

  return (
    <div
      className={`flex ${
        message.role === "user" ? "justify-end" : "justify-start"
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <GlassPanel
        className={`max-w-3xl rounded-2xl p-4 relative overflow-hidden ${
          message.role === "user"
            ? "bg-purple-900/30 border border-purple-800/50"
            : "bg-gray-800/50 border border-gray-700/50"
        }`}
      >
        {isEditing ? (
          <div className="space-y-2">
            <textarea
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              className="w-full bg-gray-900/50 border border-gray-700 rounded-lg p-3 text-white focus:outline-none focus:ring-1 focus:ring-purple-500"
              rows={4}
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsEditing(false)}
                className="px-3 py-1 text-sm text-gray-300 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-3 py-1 text-sm bg-purple-600 hover:bg-purple-700 rounded-lg"
              >
                Save
              </button>
            </div>
          </div>
        ) : (
          <div className="whitespace-pre-wrap">{message.content}</div>
        )}

        {(isHovered || isEditing) && message.role === "user" && (
          <div className="absolute top-2 right-2 flex gap-1">
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="p-1 rounded-full hover:bg-gray-700/50 transition-colors"
              title="Edit"
            >
              <FiEdit2 className="w-4 h-4" />
            </button>
            <button
              onClick={handleCopy}
              className="p-1 rounded-full hover:bg-gray-700/50 transition-colors"
              title="Copy"
            >
              {copied ? (
                <FiCheck className="w-4 h-4 text-green-400" />
              ) : (
                <FiCopy className="w-4 h-4" />
              )}
            </button>
          </div>
        )}
      </GlassPanel>
    </div>
  );
}
