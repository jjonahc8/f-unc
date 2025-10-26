"""
YouTube search utilities for finding meme explanation videos
"""

import requests
from typing import Optional, Dict, List
import json
import re


def search_youtube_videos(meme_name: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search YouTube for meme explanation videos and return top results.

    Args:
        meme_name: The name of the meme to search for
        max_results: Maximum number of results to return (default 3)

    Returns:
        List of dictionaries with video information
        [
            {
                "title": "Video title",
                "url": "https://youtube.com/watch?v=...",
                "thumbnail": "Thumbnail URL",
                "channel": "Channel name",
                "type": "video" or "shorts",
                "platform": "youtube"
            }
        ]
    """
    try:
        # Construct search query
        search_query = f"{meme_name} meme explained"
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        html_content = response.text

        # Find the ytInitialData JSON object embedded in the page
        match = re.search(r'var ytInitialData = ({.*?});', html_content)
        if not match:
            print("Could not find ytInitialData in YouTube response")
            return []

        data = json.loads(match.group(1))

        # Navigate through the JSON structure to find video results
        contents = (
            data.get('contents', {})
            .get('twoColumnSearchResultsRenderer', {})
            .get('primaryContents', {})
            .get('sectionListRenderer', {})
            .get('contents', [])
        )

        if not contents:
            return []

        results = []

        # Extract videos from the search results
        for section in contents:
            if len(results) >= max_results:
                break

            item_section = section.get('itemSectionRenderer', {})
            for item in item_section.get('contents', []):
                if len(results) >= max_results:
                    break

                # Check for regular video
                video_renderer = item.get('videoRenderer')
                if video_renderer:
                    video_id = video_renderer.get('videoId')
                    if not video_id:
                        continue

                    # Check if it's a short
                    nav_endpoint = video_renderer.get('navigationEndpoint', {})
                    command_metadata = nav_endpoint.get('commandMetadata', {})
                    web_metadata = command_metadata.get('webCommandMetadata', {})
                    url_path = web_metadata.get('url', '')
                    is_short = 'shorts' in url_path

                    # Get title
                    title_runs = video_renderer.get('title', {}).get('runs', [])
                    title = title_runs[0].get('text', 'Unknown Title') if title_runs else 'Unknown Title'

                    # Get channel name
                    owner_runs = video_renderer.get('ownerText', {}).get('runs', [])
                    channel = owner_runs[0].get('text', 'Unknown Channel') if owner_runs else 'Unknown Channel'

                    # Get thumbnail - use highest quality available
                    thumbnails = video_renderer.get('thumbnail', {}).get('thumbnails', [])
                    thumbnail = thumbnails[-1].get('url') if thumbnails else None

                    # Construct URL
                    if is_short:
                        url = f"https://www.youtube.com/shorts/{video_id}"
                        video_type = "shorts"
                    else:
                        url = f"https://www.youtube.com/watch?v={video_id}"
                        video_type = "video"

                    results.append({
                        "title": title,
                        "url": url,
                        "thumbnail": thumbnail,
                        "channel": channel,
                        "type": video_type,
                        "platform": "youtube",
                        "video_id": video_id
                    })

        return results

    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []


def get_top_youtube_video(meme_name: str) -> Optional[Dict[str, str]]:
    """
    Get the top YouTube video for a meme.

    Args:
        meme_name: The name of the meme to search for

    Returns:
        Dictionary with video information or None if not found
    """
    results = search_youtube_videos(meme_name, max_results=1)
    return results[0] if results else None
