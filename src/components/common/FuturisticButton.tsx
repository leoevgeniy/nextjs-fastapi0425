"use client";

import { ButtonHTMLAttributes, forwardRef } from "react";
import { motion, useDrag } from "framer-motion";
import cn from "classnames";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "outline" | "secondary";
  size?: "sm" | "md" | "lg";
}

export const FuturisticButton = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { children, className, variant = "primary", size = "md", ...props },
    ref
  ) => {
    const omitOnDrag = (props: ButtonProps) => {
      const { onDrag, ...filteredProps } = props;
      return filteredProps;
    };
    const filteredProps = omitOnDrag(props);
    delete filteredProps.onDragEnd;
    return (
      <motion.button
        ref={ref}
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
        className={cn(
          "relative overflow-hidden rounded-lg font-medium transition-all",
          "focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900",
          {
            "px-4 py-2 text-sm": size === "sm",
            "px-6 py-3 text-base": size === "md",
            "px-8 py-4 text-lg": size === "lg",
          },
          {
            "bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/20":
              variant === "primary",
            "bg-transparent border border-purple-500 text-purple-400 hover:bg-purple-900/30":
              variant === "outline",
            "bg-gray-800 text-gray-200 hover:bg-gray-700":
              variant === "secondary",
          },
          className
        )}
        {...filteredProps}
      >
        <span className="relative z-10">{children}</span>
        {variant === "primary" && (
          <span className="absolute inset-0 bg-gradient-to-r from-purple-500 to-blue-500 opacity-0 hover:opacity-100 transition-opacity" />
        )}
      </motion.button>
    );
  }
);

FuturisticButton.displayName = "FuturisticButton";
