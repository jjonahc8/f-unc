"""
Debug script to inspect Know Your Meme HTML structure
"""

import requests
from bs4 import BeautifulSoup

def debug_kym_search(meme_name: str):
    """Debug the Know Your Meme search to see actual HTML structure"""
    search_url = f"https://knowyourmeme.com/search?q={meme_name.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print(f"Fetching: {search_url}")
    print("="*70)

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        print("="*70)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save full HTML for inspection
        with open('debug_output.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("✅ Saved full HTML to debug_output.html")

        # Try to find search results with various selectors
        print("\n" + "="*70)
        print("SEARCHING FOR RESULT CONTAINERS...")
        print("="*70)

        # Try multiple possible selectors
        selectors_to_try = [
            ('td.photo', 'td with class photo'),
            ('table.entry_list td', 'td inside table.entry_list'),
            ('a[href*="/memes/"]', 'links containing /memes/'),
            ('div.entry', 'div with class entry'),
            ('tr.entry', 'tr with class entry'),
            ('h2 a', 'h2 links'),
            ('.entry-grid-body', 'entry-grid-body class'),
            ('.entry', '.entry class'),
        ]

        for selector, description in selectors_to_try:
            results = soup.select(selector)
            print(f"\n{description} ({selector}): Found {len(results)} elements")
            if results:
                print(f"  First element preview: {str(results[0])[:200]}...")

        # Look for any table structures
        print("\n" + "="*70)
        print("TABLES FOUND:")
        print("="*70)
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        for i, table in enumerate(tables[:3]):
            classes = table.get('class', [])
            print(f"  Table {i+1}: classes={classes}")

        # Look for divs that might contain results
        print("\n" + "="*70)
        print("DIVS WITH COMMON RESULT CLASSES:")
        print("="*70)
        common_classes = ['entry', 'result', 'search', 'item', 'card', 'grid']
        for cls in common_classes:
            divs = soup.find_all('div', class_=lambda x: x and cls in x.lower() if x else False)
            if divs:
                print(f"  Divs with '{cls}' in class: {len(divs)}")
                if divs:
                    print(f"    First div classes: {divs[0].get('class', [])}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("KNOW YOUR MEME HTML STRUCTURE DEBUGGER")
    print("="*70 + "\n")

    debug_kym_search("huzz")
