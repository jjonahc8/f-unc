export type Sociolect = "boomer" | "gen-x" | "millenial" | "gen-z";

export interface Explanation {
  meme_name: string;
  explanation: string;
}

export interface VideoResult {
  title: string;
  url: string;
  thumbnail: string;
  channel: string;
  type: string;
  platform: string;
  video_id: string;
}

export interface MediaVideosResponse {
  meme_name: string;
  youtube_videos: VideoResult[];
  total_results: number;
}
