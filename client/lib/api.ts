import { Explanation, MediaVideosResponse, Sociolect } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function explainMeme(
  topic: string,
  sociolect: Sociolect
): Promise<Explanation> {
  const response = await fetch(
    `${API_BASE_URL}/explain/explanation?topic=${encodeURIComponent(topic)}&sociolect=${sociolect}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch explanation");
  }

  return response.json();
}

export async function getMemeVideos(
  topic: string,
  maxResults: number = 4
): Promise<MediaVideosResponse> {
  const response = await fetch(
    `${API_BASE_URL}/media/videos?topic=${encodeURIComponent(topic)}&max_results=${maxResults}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch videos");
  }

  return response.json();
}
