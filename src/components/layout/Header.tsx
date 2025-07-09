"use client";

import { FiMenu, FiCommand } from "react-icons/fi";
import { UserButton } from "@/components/auth/UserButton";
import { FuturisticButton } from "@/components/common/FuturisticButton";
import { useCommandPalette } from "@/hooks/useCommandPalette";
import { motion } from "framer-motion";
import { usePathname } from "next/navigation";
import { FiPlus } from "react-icons/fi";
import Link from "next/link";

export function Header() {
  const { toggle: toggleCommandPalette } = useCommandPalette();
  const pathname = usePathname();
  const isChatPage = pathname?.startsWith("/chat");

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-40 bg-gray-900/80 backdrop-blur-md border-b border-gray-800"
    >
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left side - Mobile menu and logo */}
          <div className="flex items-center gap-4">
            <button className="md:hidden text-gray-400 hover:text-white p-1 rounded-md">
              <FiMenu className="h-6 w-6" />
            </button>

            <Link href="/" className="flex items-center">
              <div className="flex items-center">
                <div className="h-8 w-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center mr-3">
                  <FiCommand className="h-4 w-4 text-white" />
                </div>
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-blue-400">
                  AI Assistant
                </span>
              </div>
            </Link>
          </div>

          {/* Center - Navigation (hidden on mobile) */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link
              href="/chat"
              className={`text-sm font-medium transition-colors hover:text-purple-400 ${
                isChatPage ? "text-purple-400" : "text-gray-300"
              }`}
            >
              Chat
            </Link>
            <Link
              href="/analytics"
              className="text-sm font-medium text-gray-300 hover:text-purple-400 transition-colors"
            >
              Analytics
            </Link>
            <Link
              href="/templates"
              className="text-sm font-medium text-gray-300 hover:text-purple-400 transition-colors"
            >
              Templates
            </Link>
          </nav>

          {/* Right side - Actions and user */}
          <div className="flex items-center gap-4">
            {isChatPage && (
              <FuturisticButton
                size="sm"
                variant="secondary"
                className="hidden md:flex items-center gap-1"
                asChild
              >
                <Link href="/chat">
                  <FiPlus className="h-4 w-4" />
                  <span>New Chat</span>
                </Link>
              </FuturisticButton>
            )}

            <button
              onClick={toggleCommandPalette}
              className="hidden md:flex items-center justify-center h-9 w-9 rounded-md bg-gray-800 hover:bg-gray-700 transition-colors text-gray-300 hover:text-white border border-gray-700"
              aria-label="Open command palette"
            >
              <FiCommand className="h-4 w-4" />
            </button>

            <UserButton />
          </div>
        </div>
      </div>
    </motion.header>
  );
}
