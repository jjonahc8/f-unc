"use client";

import { useState } from "react";
import { Sociolect, Explanation, MediaVideosResponse } from "@/lib/types";
import { explainMeme, getMemeVideos } from "@/lib/api";
import LoadingDots from "@/components/LoadingDots";
import ResultsDisplay from "@/components/ResultsDisplay";
import VideoCollage from "@/components/VideoCollage";

const GENERATIONS: Sociolect[] = ["boomer", "gen-x", "millenial", "gen-z"];

export default function Home() {
  const [meme, setMeme] = useState("");
  const [generation, setGeneration] = useState<Sociolect>("gen-z");
  const [loading, setLoading] = useState(false);
  const [explanation, setExplanation] = useState<Explanation | null>(null);
  const [videos, setVideos] = useState<MediaVideosResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);

  const cycleGeneration = () => {
    const currentIndex = GENERATIONS.indexOf(generation);
    const nextIndex = (currentIndex + 1) % GENERATIONS.length;
    setGeneration(GENERATIONS[nextIndex]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!meme.trim()) return;

    setLoading(true);
    setError(null);
    setExplanation(null);
    setVideos(null);

    try {
      const [explanationData, videosData] = await Promise.all([
        explainMeme(meme, generation),
        getMemeVideos(meme, 3),
      ]);

      setExplanation(explanationData);
      setVideos(videosData);
      setShowResults(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setShowResults(false);
    setExplanation(null);
    setVideos(null);
    setMeme("");
  };

  return (
    <div className="min-h-screen bg-offwhite flex items-center justify-center p-8 relative">
      {/* Flowing background text */}
      <div className="flowing-text flow-1">
        brainrot brainrot brainrot brainrot brainrot brainrot brainrot brainrot
      </div>
      <div className="flowing-text flow-2">
        skibidi toilet rizz gyatt ohio sigma skibidi toilet rizz gyatt ohio sigma
      </div>
      <div className="flowing-text flow-3">
        no cap fr fr on god bussin sheesh no cap fr fr on god bussin sheesh
      </div>

      <div className="w-full max-w-6xl relative z-10">
        {/* f(unc) header - top left absolute positioning */}
        <div className="absolute top-8 left-8">
          <h1 className="text-3xl font-bold text-black">
            f(<span className="text-green">unc</span>)
          </h1>
        </div>

        {/* Main centered container */}
        <div className="bg-black rounded-3xl p-12 min-h-[600px] flex flex-col relative overflow-hidden">
          {/* Back arrow - top right */}
          {showResults && (
            <button
              onClick={handleBack}
              className="absolute top-8 right-8 text-offwhite text-3xl hover:text-green transition-colors z-10"
              aria-label="Go back"
            >
              ←
            </button>
          )}

          {/* Sliding container */}
          <div className="flex-1 flex relative">
            {/* Input form view */}
            <div
              className={`absolute inset-0 flex flex-col items-center justify-center transition-transform duration-500 ease-in-out ${
                showResults || loading ? "-translate-x-full opacity-0" : "translate-x-0 opacity-100"
              }`}
            >
              {/* Catchphrase */}
              <div className="text-center mb-12 max-w-2xl">
                <h2 className="text-5xl font-bold mb-4 text-offwhite">
                  Decode the <span className="text-green">internet</span>
                </h2>
                <p className="text-xl text-offwhite opacity-70 font-mono">
                  Interpret brainrot across generations. Because not everyone speaks Gen-Z.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="w-full flex items-center justify-center">
                <div className="flex items-center gap-4 text-2xl">
                  <span className="text-offwhite font-mono italic">uncify(</span>

                  <div className="flex items-baseline gap-2">
                    <label className="text-green font-mono">brainrot</label>
                    <span className="text-green font-mono">=</span>
                    <input
                      type="text"
                      value={meme}
                      onChange={(e) => setMeme(e.target.value)}
                      placeholder=""
                      className="bg-transparent border-b-2 border-green text-offwhite px-2 py-1 focus:outline-none focus:border-offwhite transition-colors font-mono w-40"
                    />
                  </div>

                  <span className="text-offwhite font-mono">,</span>

                  <div className="flex items-baseline gap-2">
                    <label className="text-green font-mono">your_gen</label>
                    <span className="text-green font-mono">=</span>
                    <button
                      type="button"
                      onClick={cycleGeneration}
                      className="bg-transparent border-b-2 border-green text-offwhite px-2 py-1 hover:border-offwhite transition-colors font-mono cursor-pointer min-w-[120px] text-left"
                    >
                      {generation}
                    </button>
                  </div>

                  <span className="text-offwhite font-mono">)</span>
                </div>
              </form>

              {/* Subtitle hint */}
              <div className="mt-8 text-center">
                <p className="text-offwhite opacity-50 font-mono text-sm">
                  Press Enter to decode
                </p>
              </div>
            </div>

            {/* Results view */}
            <div
              className={`absolute inset-0 transition-transform duration-500 ease-in-out ${
                showResults ? "translate-x-0 opacity-100" : "translate-x-full opacity-0"
              }`}
            >
              {explanation && videos && !loading && (
                <div className="h-full overflow-y-auto">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-4">
                    <div className="space-y-4">
                      <ResultsDisplay explanation={explanation} />
                    </div>

                    <div className="space-y-4">
                      <VideoCollage videos={videos.youtube_videos} />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Loading state */}
            {loading && (
              <div className="absolute inset-0 flex items-center justify-center transition-transform duration-500 ease-in-out">
                <LoadingDots />
              </div>
            )}

            {/* Error state */}
            {error && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-red-500 border-2 border-red-500 p-4 rounded">
                  Error: {error}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
