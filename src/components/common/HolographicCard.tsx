"use client";

import { ReactNode, useEffect, useRef } from "react";
import cn from "classnames";

interface HolographicCardProps {
  children: ReactNode;
  className?: string;
}

export function HolographicCard({ children, className }: HolographicCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!cardRef.current) return;

      const rect = cardRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      cardRef.current.style.setProperty("--mouse-x", `${x}px`);
      cardRef.current.style.setProperty("--mouse-y", `${y}px`);
    };

    const card = cardRef.current;
    card?.addEventListener("mousemove", handleMouseMove);

    return () => {
      card?.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <div
      ref={cardRef}
      className={cn(
        "relative rounded-xl overflow-hidden border border-transparent",
        "before:absolute before:inset-0 before:bg-gradient-to-br before:from-purple-600/20 before:to-blue-500/20 before:opacity-0 hover:before:opacity-100",
        "after:absolute after:inset-0 after:bg-gradient-to-br after:from-purple-600/10 after:via-transparent after:to-blue-500/10 after:opacity-0 hover:after:opacity-100",
        "transition-all duration-300 hover:border-purple-500/30",
        className
      )}
    >
      <div className="relative z-10 h-full">{children}</div>
    </div>
  );
}
