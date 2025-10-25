"""
Debug script to inspect individual meme page HTML structure
"""

import requests
from bs4 import BeautifulSoup

def debug_meme_page(meme_url: str):
    """Debug the individual meme page to see actual HTML structure"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print(f"Fetching: {meme_url}")
    print("="*70)

    try:
        response = requests.get(meme_url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        print("="*70)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save full HTML for inspection
        with open('debug_meme_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("✅ Saved full HTML to debug_meme_page.html")

        # Look for sections
        print("\n" + "="*70)
        print("SEARCHING FOR CONTENT SECTIONS...")
        print("="*70)

        sections = soup.find_all('section')
        print(f"\nFound {len(sections)} <section> elements")
        for i, section in enumerate(sections[:10]):
            section_id = section.get('id', 'no-id')
            section_class = section.get('class', [])
            print(f"  Section {i+1}: id='{section_id}', class={section_class}")

        # Look for divs with about/origin content
        print("\n" + "="*70)
        print("SEARCHING FOR ABOUT/ORIGIN CONTENT...")
        print("="*70)

        # Try different selectors
        selectors_to_try = [
            ('section#about', 'section with id about'),
            ('div#about', 'div with id about'),
            ('section#origin', 'section with id origin'),
            ('div#origin', 'div with id origin'),
            ('div.bodycopy', 'div with class bodycopy'),
            ('div.entry-details', 'div with entry details'),
        ]

        for selector, description in selectors_to_try:
            results = soup.select(selector)
            print(f"\n{description} ({selector}): Found {len(results)} elements")
            if results:
                text = results[0].get_text(strip=True)[:200]
                print(f"  Preview: {text}...")

        # Look for h2 headers that might indicate sections
        print("\n" + "="*70)
        print("H2 HEADERS (potential section markers):")
        print("="*70)
        h2_tags = soup.find_all('h2')
        for h2 in h2_tags[:10]:
            print(f"  - {h2.get_text(strip=True)}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("KNOW YOUR MEME PAGE STRUCTURE DEBUGGER")
    print("="*70 + "\n")

    debug_meme_page("https://knowyourmeme.com/memes/huzz-slang")
