"use client";

import { FiEdit2, FiTrash2, FiCopy } from "react-icons/fi";
import { renameSession } from "@/app/api/chat/client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { FuturisticButton } from "@/components/common/FuturisticButton";

interface SessionControlsProps {
  sessionId: string;
}

export function SessionControls({ sessionId }: SessionControlsProps) {
  const [isRenaming, setIsRenaming] = useState(false);
  const [newName, setNewName] = useState("");
  const router = useRouter();

  const handleRename = async () => {
    if (!newName.trim()) return;
    await renameSession(sessionId, newName);
    router.refresh();
    setIsRenaming(false);
  };

  return (
    <div className="flex gap-2">
      <button
        onClick={() => setIsRenaming(true)}
        className="p-2 text-gray-400 hover:text-purple-400 transition-colors"
        title="Rename session"
      >
        <FiEdit2 />
      </button>

      <button
        onClick={() => navigator.clipboard.writeText(sessionId)}
        className="p-2 text-gray-400 hover:text-blue-400 transition-colors"
        title="Copy session ID"
      >
        <FiCopy />
      </button>

      <Modal isOpen={isRenaming} onClose={() => setIsRenaming(false)}>
        <div className="bg-gray-800 p-6 rounded-xl space-y-4">
          <h3 className="text-lg font-medium">Rename Session</h3>
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Enter new session name"
            autoFocus
          />
          <div className="flex justify-end gap-2">
            <FuturisticButton
              onClick={() => setIsRenaming(false)}
              variant="secondary"
            >
              Cancel
            </FuturisticButton>
            <FuturisticButton onClick={handleRename} disabled={!newName.trim()}>
              Rename
            </FuturisticButton>
          </div>
        </div>
      </Modal>
    </div>
  );
}
