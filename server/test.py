# """
# Simple test script for the search_knowyourmeme function
# """

# from tools import search_knowyourmeme

# def main():
#     """Test the Know Your Meme search function"""

#     # Test with a popular meme
#     test_memes = [
#         "huzz",
#         "aura",
#         "looksmaxxing",
#         "67",
#         "fanum tax",
#         "rizzler",
#     ]

#     print("="*70)
#     print("TESTING KNOW YOUR MEME SEARCH TOOL")
#     print("="*70)

#     for meme in test_memes:
#         print(f"\n\n{'='*70}")
#         print(f"Searching for: {meme}")
#         print("="*70)

#         # Invoke the tool (LangChain tools need to be invoked)
#         result = search_knowyourmeme.invoke({"meme_name": meme})
#         print(result)

#         print("\n" + "-"*70)
#         input("Press Enter to continue to next meme...")

# if __name__ == "__main__":
#     main()

"""
Simple test script for the curator_node function
"""

from server.langgraph_pipeline import curator_node  
from server.tools import search_knowyourmeme

def main():
    """Test the Curator node on real meme data"""
    test_memes = [
        "fanum tax",
        "looksmaxxing",
        "rizzler",
    ]

    print("=" * 70)
    print("TESTING CURATOR NODE")
    print("=" * 70)

    for meme in test_memes:
        print(f"\n\n{'='*70}")
        print(f"Testing curator for: {meme}")
        print("="*70)

        # Step 1: Get raw data from KnowYourMeme
        raw_data = search_knowyourmeme.invoke({"meme_name": meme})

        # Step 2: Build initial state
        state = {
            "meme_name": meme,
            "raw_data": raw_data,
            "curated_data": {},
            "final_explanation": "",
            "sources": []
        }

        # Step 3: Run curator node
        result = curator_node(state)

        # Step 4: Print structured JSON output
        print("\n--- Curated Output ---")
        print(result["curated_data"])

        print("\n" + "-"*70)
        input("Press Enter to continue to next meme...")

if __name__ == "__main__":
    main()
