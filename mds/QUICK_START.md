# Quick Start Guide - Video Media API

Get video content for memes in 3 simple steps!

## 1. Start the Server

```bash
python -m server.api
```

Server runs on: `http://localhost:8000`

## 2. Fetch Videos

### Get All Videos (YouTube + TikTok)
```bash
curl "http://localhost:8000/media/videos?topic=stonks&max_results=3"
```

### Get YouTube Only
```bash
curl "http://localhost:8000/media/youtube?topic=drake+hotline+bling"
```

### Get TikTok Only
```bash
curl "http://localhost:8000/media/tiktok?topic=skibidi+toilet"
```

## 3. Use in Your Frontend

### Fetch from JavaScript

```javascript
// Fetch videos
const response = await fetch('http://localhost:8000/media/videos?topic=stonks&max_results=3');
const data = await response.json();

// data structure:
{
  meme_name: "stonks",
  youtube_videos: [
    {
      title: "What is Stonks meme?",
      url: "https://youtube.com/watch?v=...",
      thumbnail: "https://i.ytimg.com/vi/.../hq720.jpg",
      channel: "Channel Name",
      type: "video",
      platform: "youtube",
      video_id: "abc123"
    }
  ],
  tiktok_videos: [...],
  total_results: 6
}
```

### Display Videos

```html
<!-- Display YouTube video -->
<div class="video-card">
  <a href="${video.url}" target="_blank">
    <img src="${video.thumbnail}" alt="${video.title}">
    <h3>${video.title}</h3>
  </a>
  <p>${video.channel}</p>
</div>
```

## What You Get

Each video object contains:

✅ **title** - Video title/caption
✅ **url** - Direct clickable link
✅ **thumbnail** - Image URL (for YouTube)
✅ **channel** - Channel name/username
✅ **type** - "video", "shorts", or "short"
✅ **platform** - "youtube" or "tiktok"
✅ **video_id** - Unique identifier

## API Endpoints Summary

| Endpoint | Purpose | Returns |
|----------|---------|---------|
| `/media/videos` | Get both platforms | YouTube + TikTok videos |
| `/media/youtube` | Get YouTube only | Array of YouTube videos |
| `/media/tiktok` | Get TikTok only | Array of TikTok videos |

## Query Parameters

- `topic` (required) - The meme name to search
- `max_results` (optional) - Max results per platform (1-10, default: 3)

## Test It

```bash
# Run the test script
python server/test_video_endpoints.py

# Or visit interactive docs
open http://localhost:8000/docs
```

## Full Documentation

- **Complete API Docs**: [VIDEO_API_DOCS.md](VIDEO_API_DOCS.md)
- **General README**: [README.md](README.md)
- **Sociolect Examples**: [SOCIOLECT_EXAMPLES.md](SOCIOLECT_EXAMPLES.md)

## Example Response

```json
{
  "meme_name": "stonks",
  "youtube_videos": [
    {
      "title": "What is Stonks meme?",
      "url": "https://www.youtube.com/watch?v=myfbK8v8cLM",
      "thumbnail": "https://i.ytimg.com/vi/myfbK8v8cLM/hq720.jpg",
      "channel": "Ask About Life & How-To",
      "type": "video",
      "platform": "youtube",
      "video_id": "myfbK8v8cLM"
    }
  ],
  "tiktok_videos": [],
  "total_results": 1
}
```

---

**That's it!** You now have all the data needed to display clickable video thumbnails in your frontend. 🎉
