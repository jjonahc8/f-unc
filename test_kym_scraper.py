"""
Test script for Know Your Meme scraper
Tests the 'aura' meme search
"""

import requests
from bs4 import BeautifulSoup

def test_knowyourmeme_search(meme_name: str = "aura"):
    """Test the Know Your Meme search and scraping"""

    print("="*70)
    print(f"Testing Know Your Meme search for: '{meme_name}'")
    print("="*70)

    try:
        # Step 1: Search Know Your Meme
        search_url = f"https://knowyourmeme.com/search?q={meme_name.replace(' ', '+')}"
        print(f"\n1. Searching URL: {search_url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(search_url, headers=headers, timeout=30)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Length: {len(response.text)} characters")

        if response.status_code != 200:
            print(f"   ❌ Failed with status code: {response.status_code}")
            return

        # Step 2: Parse the search results
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try different selectors to find search results
        print("\n2. Looking for search results...")

        # Method 1: a.item links with /memes/
        search_items_1 = soup.select('a.item[href*="/memes/"]')
        print(f"   Method 1 (a.item[href*='/memes/']): Found {len(search_items_1)} results")

        # Method 2: Any link with /memes/ in href
        search_items_2 = soup.select('a[href*="/memes/"]')
        print(f"   Method 2 (a[href*='/memes/']): Found {len(search_items_2)} results")

        # Method 3: Look for table rows (old structure)
        search_items_3 = soup.select('tr[class*="entry"]')
        print(f"   Method 3 (tr[class*='entry']): Found {len(search_items_3)} results")

        # Method 4: Look for any div or article with entry/result class
        search_items_4 = soup.select('div[class*="entry"], article[class*="entry"]')
        print(f"   Method 4 (div/article with 'entry'): Found {len(search_items_4)} results")

        # Save HTML for manual inspection
        with open('kym_search_results.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\n   💾 Saved search results HTML to: kym_search_results.html")

        # Step 3: Try to find any meme links
        print("\n3. Extracting meme links...")
        all_meme_links = soup.find_all('a', href=True)
        meme_urls = []

        for link in all_meme_links:
            href = link.get('href', '')
            if '/memes/' in href and not any(skip in href for skip in ['#', 'search', 'new', 'confirmed']):
                full_url = href if href.startswith('http') else f"https://knowyourmeme.com{href}"
                if full_url not in meme_urls:
                    meme_urls.append(full_url)
                    if len(meme_urls) <= 5:
                        print(f"   - {full_url}")

        print(f"\n   Total unique meme URLs found: {len(meme_urls)}")

        if not meme_urls:
            print("\n   ❌ No meme URLs found in search results!")
            print("\n   Trying direct URL instead...")
            # Try direct URL
            direct_url = f"https://knowyourmeme.com/memes/{meme_name.lower().replace(' ', '-')}"
            print(f"   Testing: {direct_url}")

            direct_response = requests.get(direct_url, headers=headers, timeout=30)
            if direct_response.status_code == 200:
                print(f"   ✅ Direct URL works! Status: {direct_response.status_code}")
                meme_urls = [direct_url]
            else:
                print(f"   ❌ Direct URL failed with status: {direct_response.status_code}")
                return

        # Step 4: Test fetching a meme page
        if meme_urls:
            print(f"\n4. Testing first meme page...")
            test_url = meme_urls[0]
            print(f"   URL: {test_url}")

            meme_response = requests.get(test_url, headers=headers, timeout=30)
            print(f"   Status: {meme_response.status_code}")
            print(f"   Length: {len(meme_response.text)} characters")

            if meme_response.status_code == 200:
                meme_soup = BeautifulSoup(meme_response.text, 'html.parser')

                # Look for title
                title_elem = meme_soup.find('h1')
                title = title_elem.get_text(strip=True) if title_elem else "No title found"
                print(f"   Title: {title}")

                # Look for About section
                about_header = meme_soup.find('h2', id='about')
                if about_header:
                    about_p = about_header.find_next_sibling('p')
                    about_text = about_p.get_text(strip=True)[:200] if about_p else "No about text"
                    print(f"   About (first 200 chars): {about_text}")
                else:
                    print(f"   About section: Not found (tried h2#about)")
                    # Try alternative selectors
                    about_alt = meme_soup.find('section', class_='about')
                    if about_alt:
                        print(f"   Found alternative about section: section.about")

                # Look for Origin section
                origin_header = meme_soup.find('h2', id='origin')
                if origin_header:
                    origin_p = origin_header.find_next_sibling('p')
                    origin_text = origin_p.get_text(strip=True)[:200] if origin_p else "No origin text"
                    print(f"   Origin (first 200 chars): {origin_text}")
                else:
                    print(f"   Origin section: Not found (tried h2#origin)")

                # Save meme page HTML for inspection
                with open('kym_meme_page.html', 'w', encoding='utf-8') as f:
                    f.write(meme_response.text)
                print(f"\n   💾 Saved meme page HTML to: kym_meme_page.html")

                print("\n✅ Test completed successfully!")
            else:
                print(f"   ❌ Failed to fetch meme page")

    except requests.Timeout:
        print("\n❌ Request timed out!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with 'aura'
    test_knowyourmeme_search("aura")

    print("\n" + "="*70)
    print("Test complete! Check the saved HTML files to debug further.")
    print("="*70)
