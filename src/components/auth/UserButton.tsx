"use client";

import { FiUser } from "react-icons/fi";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/DropdownMenu";
import { useRouter } from "next/navigation";

export function UserButton() {
  const router = useRouter();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="h-9 w-9 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center text-gray-300 hover:text-white transition-colors">
          <FiUser className="h-4 w-4" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        align="end"
        className="w-56 bg-gray-800 border border-gray-700 rounded-md shadow-lg"
      >
        <DropdownMenuItem
          className="cursor-pointer focus:bg-gray-700 text-gray-300"
          onClick={() => router.push("/profile")}
        >
          Profile
        </DropdownMenuItem>
        <DropdownMenuItem
          className="cursor-pointer focus:bg-gray-700 text-gray-300"
          onClick={() => router.push("/settings")}
        >
          Settings
        </DropdownMenuItem>
        <DropdownMenuItem
          className="cursor-pointer focus:bg-red-900/50 text-red-400"
          onClick={() => router.push("/logout")}
        >
          Log Out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
