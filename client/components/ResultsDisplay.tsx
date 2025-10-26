import { Explanation } from "@/lib/types";

interface ResultsDisplayProps {
  explanation: Explanation;
}

export default function ResultsDisplay({ explanation }: ResultsDisplayProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2 text-green">
          Brainrot: <span className="text-offwhite">{explanation.meme_name}</span>
        </h2>
      </div>

      <div>
        <h3 className="text-2xl font-semibold mb-3 text-green">Explanation</h3>
        <p className="text-offwhite leading-relaxed whitespace-pre-wrap">
          {explanation.explanation}
        </p>
      </div>
    </div>
  );
}
