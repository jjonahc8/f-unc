import { VideoResult } from "@/lib/types";

interface VideoCollageProps {
  videos: VideoResult[];
}

export default function VideoCollage({ videos }: VideoCollageProps) {
  if (videos.length === 0) return null;

  const getEmbedUrl = (video: VideoResult) => {
    return `https://www.youtube.com/embed/${video.video_id}`;
  };

  return (
    <div className="grid grid-cols-2 gap-4 auto-rows-fr">
      {videos.map((video, index) => (
        <div
          key={video.video_id}
          className={`relative rounded-lg overflow-hidden border-2 border-green ${
            index === 0 ? "col-span-2 row-span-2" : ""
          }`}
          style={{ minHeight: index === 0 ? "280px" : "200px" }}
        >
          <iframe
            src={getEmbedUrl(video)}
            title={video.title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="w-full h-full absolute inset-0"
          />
        </div>
      ))}
    </div>
  );
}
