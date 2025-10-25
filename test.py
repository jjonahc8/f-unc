"""
Simple test script for the search_knowyourmeme function
"""

from tools import search_knowyourmeme

def main():
    """Test the Know Your Meme search function"""

    # Test with a popular meme
    test_memes = [
        "huzz",
        "aura",
        "looksmaxxing",
        "67",
        "fanum tax",
        "rizzler",
    ]

    print("="*70)
    print("TESTING KNOW YOUR MEME SEARCH TOOL")
    print("="*70)

    for meme in test_memes:
        print(f"\n\n{'='*70}")
        print(f"Searching for: {meme}")
        print("="*70)

        # Invoke the tool (LangChain tools need to be invoked)
        result = search_knowyourmeme.invoke({"meme_name": meme})
        print(result)

        print("\n" + "-"*70)
        input("Press Enter to continue to next meme...")

if __name__ == "__main__":
    main()
