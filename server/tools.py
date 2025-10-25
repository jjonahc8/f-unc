"""
Tools for meme search and analysis
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from langchain.tools import tool
from openai import OpenAI
from pydantic import BaseModel, Field, HttpUrl

    

class MemeExplanation(BaseModel):
    """Structured response for meme format explanations"""
    meme_name: str
    url: str
    about: str
    origin: str

class KnowYourMemeResult(BaseModel):
    """ List of MemeExplanation results """
    results: List[MemeExplanation]


@tool
def search_knowyourmeme(meme_name: str) -> str:
    """
    Search Know Your Meme (knowyourmeme.com) for meme explanations.
    Returns detailed information about the meme including origin, spread, and examples.

    Args:
        meme_name: The name of the meme to search for
    """
    try:
        # Search Know Your Meme
        search_url = f"https://knowyourmeme.com/search?q={meme_name.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find search results - updated for new HTML structure
        results = []

        # Look for search results in the "Entries" tab
        search_items = soup.select('a.item[href*="/memes/"]')[:5]  # Get top 5 results

        for item in search_items:
            # Extract the meme URL and title
            meme_url = f"https://knowyourmeme.com{item['href']}"
            title = item.get('data-title', 'Unknown')

            # If no data-title, try getting text content
            if title == 'Unknown':
                title = item.get_text(strip=True).split('\n')[0] if item.get_text(strip=True) else "Unknown"

            # Fetch the individual meme page
            try:
                meme_response = requests.get(meme_url, headers=headers, timeout=10)
                meme_response.raise_for_status()
                meme_soup = BeautifulSoup(meme_response.text, 'html.parser')

                # Extract key sections
                about = ""
                origin = ""

                # Look for About section (h2 with id='about')
                about_header = meme_soup.find('h2', id='about')
                if about_header:
                    # Get the next sibling paragraph
                    about_p = about_header.find_next_sibling('p')
                    if about_p:
                        about = about_p.get_text(strip=True)[:800]

                # Look for Origin section (h2 with id='origin')
                origin_header = meme_soup.find('h2', id='origin')
                if origin_header:
                    # Get the next sibling paragraph
                    origin_p = origin_header.find_next_sibling('p')
                    if origin_p:
                        origin = origin_p.get_text(strip=True)[:800]

                results.append(
                    MemeExplanation(
                    meme_name=title,
                    url=meme_url,
                    about=about or "No description available",
                    origin=origin or "No origin information available"
                    )
                )

            except Exception as e:
                print(f"Error fetching meme page: {e}")
                continue

        if not results:
            return f"No results found on Know Your Meme for '{meme_name}'."

        # Format output as string for LLM consumption
        output = f"Know Your Meme results for '{meme_name}':\n\n"
        # Output only contains content from top 3 results
        for i, result in enumerate(results[:3], 1):
            output += f"{i}. {result.meme_name}\n"
            output += f"   URL: {result.url}\n\n"
            output += f"   ABOUT:\n   {result.about}\n\n"
            if result.origin:
                output += f"   ORIGIN:\n   {result.origin}\n\n"
            output += "-" * 70 + "\n\n"

        return output

    except Exception as e:
        return f"Error searching Know Your Meme: {str(e)}"


@tool
def explain_meme_format(meme_name: str, examples: str) -> str:
    """
    Use AI to explain what a meme format means, its origin, and how it's used.

    Args:
        meme_name: The name of the meme format
        examples: Context and examples from Reddit search
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""You are a meme culture expert. Explain the '{meme_name}' meme format.

Context from Reddit:
{examples}

Provide a comprehensive explanation including:
1. **Format Description**: What does this meme look like? What's the template?
2. **Origin**: Where did it come from? When did it become popular?
3. **Meaning/Usage**: How is it typically used? What message does it convey?
4. **Examples**: Describe how the format works with examples
5. **Cultural Context**: Why is it popular? What makes it funny/relatable?

Write in a clear, educational style that anyone can understand."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content


@tool
def save_meme_explanation(content: str, filename: str = "meme_explanation.txt") -> str:
    """
    Save the meme explanation to a file.

    Args:
        content: The explanation content to save
        filename: Name of the file to save to
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully saved explanation to {filename}"
    except Exception as e:
        return f"Error saving file: {e}"


