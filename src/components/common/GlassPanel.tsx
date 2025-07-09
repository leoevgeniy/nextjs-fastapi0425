"use client";

import { ReactNode } from "react";
import { motion } from "framer-motion";
import cn from "classnames";

interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  hoverEffect?: boolean;
}

export function GlassPanel({
  children,
  className,
  hoverEffect = true,
}: GlassPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn(
        "rounded-xl border border-gray-700/50 backdrop-blur-lg",
        "bg-gradient-to-br from-gray-800/50 to-gray-900/50",
        "shadow-lg overflow-hidden",
        {
          "hover:border-purple-500/30 hover:shadow-purple-500/10 transition-all duration-300":
            hoverEffect,
        },
        className
      )}
    >
      {children}
    </motion.div>
  );
}
