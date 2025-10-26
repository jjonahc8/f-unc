"""
Sociolect Context Manager using ChromaDB Cloud
Stores and retrieves generation-specific language patterns, keywords, and examples
"""

import chromadb
from typing import List, Dict
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the server directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class SociolectContextManager:
    """
    Manages ChromaDB Cloud collections for different sociolects (generations).
    Stores and retrieves language patterns, keywords, phrases, and tone examples.

    Uses ChromaDB Cloud only - no local database support.
    """

    def __init__(
        self,
        api_key: str = None,
        tenant: str = None,
        database: str = None
    ):
        """
        Initialize ChromaDB Cloud client and collections

        Args:
            api_key: ChromaDB Cloud API key (from environment if not provided)
            tenant: Tenant ID for ChromaDB Cloud (from environment if not provided)
            database: Database name for ChromaDB Cloud (from environment if not provided)
        """
        # Get connection details from environment or parameters
        api_key = api_key or os.getenv("CHROMA_API_KEY")
        tenant = tenant or os.getenv("CHROMA_TENANT")
        database = database or os.getenv("CHROMA_DATABASE")

        # Validate required credentials
        if not api_key:
            raise ValueError("CHROMA_API_KEY is required. Set it in .env file.")
        if not tenant:
            raise ValueError("CHROMA_TENANT is required. Set it in .env file.")
        if not database:
            raise ValueError("CHROMA_DATABASE is required. Set it in .env file.")

        print(f"🌐 Connecting to ChromaDB Cloud...")
        print(f"   Tenant: {tenant}")
        print(f"   Database: {database}")

        # Initialize ChromaDB Cloud client
        try:
            self.client = chromadb.CloudClient(
                api_key=api_key,
                tenant=tenant,
                database=database
            )
            print(f"✅ Connected to ChromaDB Cloud successfully!")
        except Exception as e:
            print(f"❌ Failed to connect to ChromaDB Cloud: {e}")
            raise

        # Collection names for each sociolect
        self.collections = {}
        self.sociolects = ["boomer", "gen-x", "millenial", "gen-z"]

        # Initialize collections for each sociolect
        print(f"📚 Initializing collections...")
        for sociolect in self.sociolects:
            self.collections[sociolect] = self.client.get_or_create_collection(
                name=f"sociolect_{sociolect}",
                metadata={"description": f"Language patterns for {sociolect}"}
            )
        print(f"✅ Collections ready!")

    def add_language_patterns(
        self,
        sociolect: str,
        patterns: List[Dict[str, str]]
    ):
        """
        Add language patterns to a sociolect collection

        Args:
            sociolect: Target generation (boomer, gen-x, millenial, gen-z)
            patterns: List of pattern dictionaries with 'text', 'category', 'context' keys

        Example:
            patterns = [
                {
                    "text": "That's totally rad!",
                    "category": "expression",
                    "context": "showing enthusiasm"
                }
            ]
        """
        if sociolect not in self.collections:
            raise ValueError(f"Invalid sociolect: {sociolect}")

        collection = self.collections[sociolect]

        # Prepare data for ChromaDB
        documents = [p["text"] for p in patterns]
        metadatas = [
            {
                "category": p.get("category", "general"),
                "context": p.get("context", ""),
                "sociolect": sociolect
            }
            for p in patterns
        ]
        ids = [f"{sociolect}_{i}_{p.get('category', 'general')}" for i, p in enumerate(patterns)]

        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query_context(
        self,
        sociolect: str,
        query: str,
        n_results: int = 5,
        category_filter: str = None
    ) -> List[Dict]:
        """
        Query language patterns relevant to a topic for a specific sociolect

        Args:
            sociolect: Target generation
            query: Search query (e.g., meme name or topic)
            n_results: Number of results to return
            category_filter: Optional filter by category (keywords, phrases, tone, etc.)

        Returns:
            List of relevant language patterns with metadata
        """
        if sociolect not in self.collections:
            raise ValueError(f"Invalid sociolect: {sociolect}")

        collection = self.collections[sociolect]

        # Build where clause for filtering
        where_clause = None
        if category_filter:
            where_clause = {"category": category_filter}

        # Query the collection
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause if where_clause else None
        )

        # Format results
        formatted_results = []
        if results and results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    "text": doc,
                    "category": results['metadatas'][0][i].get("category", "general"),
                    "context": results['metadatas'][0][i].get("context", ""),
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })

        return formatted_results

    def get_all_patterns(self, sociolect: str) -> List[Dict]:
        """
        Get all language patterns for a sociolect

        Args:
            sociolect: Target generation

        Returns:
            List of all patterns
        """
        if sociolect not in self.collections:
            raise ValueError(f"Invalid sociolect: {sociolect}")

        collection = self.collections[sociolect]

        # Get all items (peek with large limit)
        results = collection.get()

        formatted_results = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents']):
                formatted_results.append({
                    "text": doc,
                    "category": results['metadatas'][i].get("category", "general"),
                    "context": results['metadatas'][i].get("context", "")
                })

        return formatted_results

    def clear_collection(self, sociolect: str):
        """Clear all data from a sociolect collection"""
        if sociolect not in self.collections:
            raise ValueError(f"Invalid sociolect: {sociolect}")

        # Delete and recreate collection
        self.client.delete_collection(f"sociolect_{sociolect}")
        self.collections[sociolect] = self.client.get_or_create_collection(
            name=f"sociolect_{sociolect}",
            metadata={"description": f"Language patterns for {sociolect}"}
        )

    def get_formatted_context(self, sociolect: str, query: str, n_results: int = 5) -> str:
        """
        Get formatted context string for use in LLM prompts

        Args:
            sociolect: Target generation
            query: Search query
            n_results: Number of results

        Returns:
            Formatted string with language patterns grouped by category
        """
        results = self.query_context(sociolect, query, n_results)

        if not results:
            return "No specific language patterns found."

        # Group by category
        grouped = {}
        for result in results:
            category = result['category']
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(result)

        # Format output
        output_lines = [f"Language patterns for {sociolect}:"]

        for category, patterns in grouped.items():
            output_lines.append(f"\n{category.upper()}:")
            for pattern in patterns:
                context_str = f" (use when: {pattern['context']})" if pattern['context'] else ""
                output_lines.append(f"  - {pattern['text']}{context_str}")

        return "\n".join(output_lines)


# =============================================================================
# SEED DATA - Generation-specific language patterns
# =============================================================================

def seed_sociolect_data(manager: SociolectContextManager):
    """
    Populate ChromaDB with example language patterns for each generation
    """

    # BOOMER (1946-1964) - Formal, traditional references
    boomer_patterns = [
        {"text": "back in my day", "category": "phrase", "context": "referencing the past"},
        {"text": "newfangled", "category": "keyword", "context": "describing new technology"},
        {"text": "the younger generation", "category": "phrase", "context": "talking about youth"},
        {"text": "it's similar to when we had...", "category": "phrase", "context": "making comparisons"},
        {"text": "on television", "category": "phrase", "context": "referencing media"},
        {"text": "the kids these days", "category": "phrase", "context": "discussing trends"},
        {"text": "quite popular", "category": "phrase", "context": "showing approval"},
        {"text": "proper grammar", "category": "tone", "context": "use formal, complete sentences"},
        {"text": "respectful tone", "category": "tone", "context": "maintain professional distance"},
        {"text": "clear explanations", "category": "tone", "context": "avoid assumptions about internet knowledge"},
    ]

    # GEN X (1965-1980) - Cynical, pop culture savvy
    genx_patterns = [
        {"text": "whatever", "category": "keyword", "context": "showing indifference"},
        {"text": "it's like [90s reference]", "category": "phrase", "context": "making comparisons"},
        {"text": "basically", "category": "keyword", "context": "simplifying explanations"},
        {"text": "pretty much", "category": "phrase", "context": "casual agreement"},
        {"text": "sort of like", "category": "phrase", "context": "making comparisons"},
        {"text": "went viral", "category": "phrase", "context": "describing spread"},
        {"text": "it's a thing now", "category": "phrase", "context": "accepting trends"},
        {"text": "semi-formal tone", "category": "tone", "context": "conversational but clear"},
        {"text": "light cynicism", "category": "tone", "context": "slightly skeptical humor acceptable"},
        {"text": "pop culture refs", "category": "tone", "context": "reference 90s/2000s culture"},
    ]

    # MILLENNIAL (1981-1996) - Internet native, informal but articulate
    millennial_patterns = [
        {"text": "lowkey", "category": "keyword", "context": "downplaying something"},
        {"text": "highkey", "category": "keyword", "context": "emphasizing something"},
        {"text": "literally", "category": "keyword", "context": "emphasizing (often hyperbolic)"},
        {"text": "tbh", "category": "keyword", "context": "being honest"},
        {"text": "ngl", "category": "keyword", "context": "not gonna lie - being candid"},
        {"text": "it's giving", "category": "phrase", "context": "describing vibes"},
        {"text": "the vibes", "category": "keyword", "context": "describing atmosphere/feeling"},
        {"text": "iconic", "category": "keyword", "context": "showing strong approval"},
        {"text": "that's so [year]", "category": "phrase", "context": "dating something"},
        {"text": "casual tone", "category": "tone", "context": "friendly, conversational"},
        {"text": "internet fluent", "category": "tone", "context": "assume familiarity with online culture"},
        {"text": "self-aware humor", "category": "tone", "context": "meta jokes acceptable"},
    ]

    # GEN Z (1997-2012) - Hyper-online, abbreviated, ironic
    genz_patterns = [
        {"text": "fr fr", "category": "keyword", "context": "for real - emphasizing truth"},
        {"text": "no cap", "category": "phrase", "context": "not lying"},
        {"text": "deadass", "category": "keyword", "context": "seriously"},
        {"text": "hits different", "category": "phrase", "context": "uniquely impactful"},
        {"text": "it's giving", "category": "phrase", "context": "describing energy/vibe"},
        {"text": "slay", "category": "keyword", "context": "doing something well"},
        {"text": "ate and left no crumbs", "category": "phrase", "context": "did something perfectly"},
        {"text": "unhinged", "category": "keyword", "context": "chaotic in a good way"},
        {"text": "rent free", "category": "phrase", "context": "can't stop thinking about"},
        {"text": "understood the assignment", "category": "phrase", "context": "did it perfectly"},
        {"text": "the way that", "category": "phrase", "context": "emphasizing a point"},
        {"text": "not the [thing]", "category": "phrase", "context": "expressing surprise"},
        {"text": "very informal", "category": "tone", "context": "extremely casual language"},
        {"text": "ironic humor", "category": "tone", "context": "embrace absurdist humor"},
        {"text": "brevity", "category": "tone", "context": "keep it short and punchy"},
    ]

    # Add all patterns to ChromaDB
    manager.add_language_patterns("boomer", boomer_patterns)
    manager.add_language_patterns("gen-x", genx_patterns)
    manager.add_language_patterns("millenial", millennial_patterns)
    manager.add_language_patterns("gen-z", genz_patterns)

    print("✅ Seeded ChromaDB with sociolect language patterns")


# =============================================================================
# MAIN - For testing
# =============================================================================

if __name__ == "__main__":
    # Initialize manager
    manager = SociolectContextManager()

    # Seed with example data
    print("Seeding database...")
    seed_sociolect_data(manager)

    # Test queries
    print("\n" + "="*70)
    print("Testing context retrieval")
    print("="*70)

    test_meme = "skibidi toilet"

    for sociolect in ["boomer", "gen-x", "millenial", "gen-z"]:
        print(f"\n--- {sociolect.upper()} ---")
        context = manager.get_formatted_context(sociolect, test_meme, n_results=5)
        print(context)
