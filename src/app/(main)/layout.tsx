import { Sidebar } from "@/components/layout/Sidebar";
import { CommandPalette } from "@/components/ui/CommandPalette";
import { GlassPanel } from "@/components/common/GlassPanel";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <Sidebar />

      <main className="flex-1 flex flex-col p-6 space-y-6 overflow-hidden">
        <GlassPanel className="flex-1 overflow-hidden">{children}</GlassPanel>
      </main>

      <CommandPalette />
    </div>
  );
}
