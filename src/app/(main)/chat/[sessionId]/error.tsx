"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 p-6">
      <h2 className="text-2xl font-bold text-red-400 mb-4">
        Failed to create chat session
      </h2>
      <p className="text-gray-300 mb-6">{error.message}</p>
      <button
        onClick={() => reset()}
        className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
      >
        Try Again
      </button>
    </div>
  );
}
