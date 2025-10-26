"""
REST API for Meme Explanation Service
Provides endpoint to explain memes based on topic and sociolect (generation)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import uvicorn

from server.langgraph_pipeline import create_meme_research_graph
from server.youtube_utils import search_youtube_videos, get_top_youtube_video


# =============================================================================
# 1. RESPONSE MODELS
# =============================================================================

class Explanation(BaseModel):
    """Response model for meme explanation endpoint"""
    meme_name: str = Field(..., description="Official name of the meme")
    explanation: str = Field(..., description="Comprehensive explanation of the meme")


class VideoResult(BaseModel):
    """Response model for a single video result"""
    title: str = Field(..., description="Video title or caption")
    url: str = Field(..., description="Direct link to the video")
    thumbnail: str = Field(..., description="URL to video thumbnail image")
    channel: str = Field(..., description="Channel name or username")
    type: str = Field(..., description="Type of video (video, shorts, short)")
    platform: str = Field(..., description="Platform (youtube, tiktok)")
    video_id: str = Field(..., description="Unique video identifier")


class MediaVideosResponse(BaseModel):
    """Response model for media videos endpoint"""
    meme_name: str = Field(..., description="The meme topic searched")
    youtube_videos: List[VideoResult] = Field(default=[], description="YouTube video results")
    total_results: int = Field(..., description="Total number of videos")


# =============================================================================
# 2. SOCIOLECT (GENERATION) ENUM
# =============================================================================

class Sociolect(str, Enum):
    """Valid sociolect/generation values"""
    BOOMER = "boomer"
    GEN_X = "gen-x"
    MILLENIAL = "millenial"
    GEN_Z = "gen-z"


# =============================================================================
# 3. INITIALIZE FASTAPI APP
# =============================================================================

app = FastAPI(
    title="Meme Explanation API",
    description="API for explaining internet memes to different generations",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# 4. INITIALIZE LANGGRAPH PIPELINE
# =============================================================================

# Create the graph once at startup
meme_graph = create_meme_research_graph()


# =============================================================================
# 5. API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "Meme Explanation API",
        "version": "1.0.0"
    }


@app.get("/explain/explanation", response_model=Explanation)
async def explain_meme(
    topic: str = Query(..., description="The meme topic/name to explain"),
    sociolect: Sociolect = Query(..., description="Target generation: boomer, gen-x, millenial, or gen-z")
):
    """
    Explain a meme topic tailored to a specific generation/sociolect

    Args:
        topic: The name of the meme to explain (e.g., "skibidi toilet")
        sociolect: Target audience generation (boomer, gen-x, millenial, gen-z)

    Returns:
        Explanation object with meme details, explanation, sources, and media
    """
    try:
        # Initialize state for the pipeline
        initial_state = {
            "meme_name": topic,
            "sociolect": sociolect.value,  # Pass the sociolect to tailor the explanation
            "raw_data": "",
            "curated_data": {},
            "final_explanation": "",
            "sources": []
        }

        # Run the LangGraph pipeline
        final_state = meme_graph.invoke(initial_state)

        # Extract data from final state
        curated_data = final_state.get("curated_data", {})
        meme_name = curated_data.get("name", topic)
        explanation = final_state.get("final_explanation", "")
        sources = final_state.get("sources", [])

        # Construct the response
        response = Explanation(
            meme_name=meme_name,
            explanation=explanation
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing meme explanation: {str(e)}"
        )


@app.get("/media/videos", response_model=MediaVideosResponse)
async def get_meme_videos(
    topic: str = Query(..., description="The meme topic to search videos for"),
    max_results: int = Query(3, ge=1, le=10, description="Maximum results (1-10)")
):
    """
    Fetch YouTube video content for a meme topic.

    Returns video data including:
    - Title
    - URL (clickable link)
    - Thumbnail URL (for display)
    - Channel/Username
    - Platform

    Args:
        topic: The meme name to search for
        max_results: Maximum number of results (default 3, max 10)

    Returns:
        MediaVideosResponse with YouTube video results
    """
    try:
        # Search YouTube
        youtube_results = search_youtube_videos(topic, max_results=max_results)

        # Convert to VideoResult models
        youtube_videos = [VideoResult(**video) for video in youtube_results]

        return MediaVideosResponse(
            meme_name=topic,
            youtube_videos=youtube_videos,
            total_results=len(youtube_videos)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching videos: {str(e)}"
        )


@app.get("/media/youtube", response_model=List[VideoResult])
async def get_youtube_videos(
    topic: str = Query(..., description="The meme topic to search for"),
    max_results: int = Query(3, ge=1, le=10, description="Maximum results (1-10)")
):
    """
    Fetch only YouTube videos for a meme topic.

    Args:
        topic: The meme name to search for
        max_results: Maximum number of results (default 3, max 10)

    Returns:
        List of YouTube video results
    """
    try:
        youtube_results = search_youtube_videos(topic, max_results=max_results)
        return [VideoResult(**video) for video in youtube_results]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching YouTube videos: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "pipeline": "ready",
        "endpoints": {
            "explain": "/explain/explanation?topic={topic}&sociolect={sociolect}",
            "videos": "/media/videos?topic={topic}",
            "youtube": "/media/youtube?topic={topic}"
        }
    }


# =============================================================================
# 6. MAIN ENTRY POINT
# =============================================================================

def main():
    """Run the API server"""
    uvicorn.run(
        "server.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
