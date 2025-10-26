"use client";

import { useState, useEffect } from "react";

const THINKING_WORDS = [
  "decoding brainrot...",
  "analyzing memes...",
  "translating vibes...",
  "processing rizz...",
  "understanding the skibidi...",
  "consulting the elders...",
  "checking knowyourmeme...",
  "no cap, still loading...",
  "bussin' through data...",
  "fr fr, almost there...",
];

export default function LoadingDots() {
  const [currentWord, setCurrentWord] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentWord((prev) => (prev + 1) % THINKING_WORDS.length);
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center gap-8 h-full">
      {/* Three dots */}
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 bg-green rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        <div className="w-4 h-4 bg-green rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        <div className="w-4 h-4 bg-green rounded-full animate-bounce"></div>
      </div>

      {/* Thinking word */}
      <div className="text-offwhite font-mono text-lg opacity-70 animate-pulse">
        {THINKING_WORDS[currentWord]}
      </div>
    </div>
  );
}
