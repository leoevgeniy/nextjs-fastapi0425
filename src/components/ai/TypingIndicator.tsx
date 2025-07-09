export function TypingIndicator() {
  return (
    <div className="flex items-center space-x-1 px-4 py-2">
      <div
        className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"
        style={{ animationDelay: "0ms" }}
      />
      <div
        className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"
        style={{ animationDelay: "150ms" }}
      />
      <div
        className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"
        style={{ animationDelay: "300ms" }}
      />
      <span className="ml-2 text-sm text-gray-400">AI is thinking...</span>
    </div>
  );
}
