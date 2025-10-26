# API Summary - Complete Endpoint Reference

Your REST API is now running with **6 endpoints** across **2 main features**:

## 🎯 Feature 1: Meme Explanations

### GET `/explain/explanation`
Generate tailored meme explanations for different generations.

**Params:**
- `topic` - Meme name (required)
- `sociolect` - Target generation: `boomer`, `gen-x`, `millenial`, `gen-z` (required)

**Returns:**
```json
{
  "meme_name": "string",
  "explanation": "string (tailored to generation)",
  "sources": ["url1", "url2"],
  "media_url": "string",
  "media_type": "string"
}
```

**Example:**
```bash
curl "http://localhost:8000/explain/explanation?topic=stonks&sociolect=boomer"
```

---

## 📹 Feature 2: Video Media Fetching

### GET `/media/videos`
Fetch both YouTube and TikTok videos in one request.

**Params:**
- `topic` - Meme name (required)
- `max_results` - Max per platform: 1-10 (optional, default: 3)

**Returns:**
```json
{
  "meme_name": "string",
  "youtube_videos": [VideoResult],
  "tiktok_videos": [VideoResult],
  "total_results": number
}
```

### GET `/media/youtube`
Fetch YouTube videos only.

**Returns:** Array of `VideoResult`

### GET `/media/tiktok`
Fetch TikTok videos only.

**Returns:** Array of `VideoResult`

### VideoResult Structure:
```json
{
  "title": "Video title",
  "url": "https://youtube.com/watch?v=...",
  "thumbnail": "https://i.ytimg.com/vi/.../hq720.jpg",
  "channel": "Channel Name",
  "type": "video | shorts | short",
  "platform": "youtube | tiktok",
  "video_id": "abc123"
}
```

**Examples:**
```bash
# All platforms
curl "http://localhost:8000/media/videos?topic=stonks&max_results=3"

# YouTube only
curl "http://localhost:8000/media/youtube?topic=drake+hotline+bling"

# TikTok only
curl "http://localhost:8000/media/tiktok?topic=skibidi+toilet"
```

---

## 🔧 Utility Endpoints

### GET `/health`
Health check with endpoint list.

```json
{
  "status": "healthy",
  "pipeline": "ready",
  "endpoints": {...}
}
```

### GET `/`
Root endpoint with API info.

---

## 🚀 Quick Test Commands

```bash
# Test explanation
curl "http://localhost:8000/explain/explanation?topic=stonks&sociolect=gen-z"

# Test all videos
curl "http://localhost:8000/media/videos?topic=stonks&max_results=3"

# Test YouTube
curl "http://localhost:8000/media/youtube?topic=drake+hotline+bling&max_results=2"

# Test health
curl "http://localhost:8000/health"
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Main documentation |
| [VIDEO_API_DOCS.md](VIDEO_API_DOCS.md) | Complete video API docs + frontend examples |
| [QUICK_START.md](QUICK_START.md) | Quick start guide for video API |
| [SOCIOLECT_EXAMPLES.md](SOCIOLECT_EXAMPLES.md) | Sociolect feature explanation |
| [API_SUMMARY.md](API_SUMMARY.md) | This file - quick reference |

---

## 🧪 Test Scripts

```bash
# Test meme explanations
python server/test_api.py

# Test video endpoints
python server/test_video_endpoints.py

# Test sociolect differences
python server/test_sociolects.py
```

---

## 💻 Frontend Integration

### Fetch Videos:
```javascript
const response = await fetch('http://localhost:8000/media/videos?topic=stonks');
const { youtube_videos, tiktok_videos } = await response.json();
```

### Display Video:
```html
<a href="${video.url}" target="_blank">
  <img src="${video.thumbnail}" alt="${video.title}">
  <h3>${video.title}</h3>
</a>
<p>${video.channel}</p>
```

See [VIDEO_API_DOCS.md](VIDEO_API_DOCS.md) for complete React/Vue/JS examples.

---

## 🔗 Interactive Docs

Visit these URLs while server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📦 What You Get from Video Endpoints

Perfect for frontend display:

✅ **Clickable URLs** - Direct links to videos
✅ **Thumbnails** - High-quality image URLs (YouTube)
✅ **Titles** - Video titles/captions
✅ **Channel Info** - Creator names
✅ **Platform Tags** - YouTube/TikTok identification
✅ **Video Types** - Regular videos vs Shorts

---

## 🎨 Example Use Case

**User Flow:**
1. User searches for meme "stonks"
2. Frontend calls `/explain/explanation?topic=stonks&sociolect=gen-z`
3. Display explanation text
4. Frontend calls `/media/videos?topic=stonks&max_results=3`
5. Display video grid with thumbnails and links
6. User clicks video → Opens in new tab

**Result:** Complete meme education experience with text explanation + video content!

---

## Server Info

- **URL**: http://localhost:8000
- **Port**: 8000
- **Auto-reload**: Enabled
- **CORS**: Enabled for all origins
