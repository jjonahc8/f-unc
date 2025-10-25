"""
Quick test without interactive prompts
"""

from tools import search_knowyourmeme

def main():
    """Test the Know Your Meme search function"""

    print("="*70)
    print("TESTING KNOW YOUR MEME SEARCH TOOL")
    print("="*70)

    # Test with huzz
    print(f"\n{'='*70}")
    print(f"Searching for: huzz")
    print("="*70)

    result = search_knowyourmeme.invoke({"meme_name": "huzz"})
    print(result)

    # Test with drake meme
    print(f"\n{'='*70}")
    print(f"Searching for: drake meme")
    print("="*70)

    result = search_knowyourmeme.invoke({"meme_name": "aura"})
    print(result)

if __name__ == "__main__":
    main()
