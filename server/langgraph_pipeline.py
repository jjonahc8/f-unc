"""
LangGraph Multi-Agent Pipeline for Meme Analysis
Researcher → Curator → Explainer

This creates a structured pipeline where:
1. Researcher: Searches Know Your Meme for raw data
2. Curator: Filters and organizes the best information
3. Explainer: Generates final comprehensive explanation
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from server.tools import search_knowyourmeme
from server.sociolect_context import SociolectContextManager, seed_sociolect_data
import json

load_dotenv()

# Initialize ChromaDB Cloud context manager
try:
    context_manager = SociolectContextManager()

    # Seed with language patterns if database is empty
    # Check if we need to seed by trying to get patterns for gen-z
    if not context_manager.get_all_patterns("gen-z"):
        print("🌱 Initializing sociolect language patterns database...")
        seed_sociolect_data(context_manager)
except Exception as e:
    print(f"⚠️  Error initializing ChromaDB Cloud: {e}")
    print("Please check your CHROMA_API_KEY, CHROMA_TENANT, and CHROMA_DATABASE in .env")
    raise


# =============================================================================
# 1. DEFINE STATE SCHEMA
# =============================================================================

class MemeResearchState(TypedDict):
    """State that flows through the agent pipeline"""
    meme_name: str
    sociolect: str  # Target generation: boomer, gen-x, millenial, gen-z
    raw_data: str  # From Researcher
    curated_data: dict  # From Curator
    final_explanation: str  # From Explainer
    sources: list[str]  # URLs collected

# =============================================================================
# 2. RESEARCHER AGENT - Searches Know Your Meme
# =============================================================================

def researcher_node(state: MemeResearchState) -> MemeResearchState:
    """
    Researcher Agent: Searches Know Your Meme for raw meme data
    """
    print("\n🔍 RESEARCHER: Searching Know Your Meme...")

    meme_name = state["meme_name"]

    # Use the search_knowyourmeme tool
    raw_data = search_knowyourmeme.invoke({"meme_name": meme_name})

    print(f"✓ Found {len(raw_data)} characters of data")

    return {
        **state,
        "raw_data": raw_data,
        "sources": []  # Will be populated by curator
    }


# =============================================================================
# 3. CURATOR AGENT - Organizes and filters information
# =============================================================================

def curator_node(state: MemeResearchState) -> MemeResearchState:
    """
    Curator Agent: Extracts and structures the most important information
    """
    print("\n📋 CURATOR: Organizing and filtering data...")

    # Debug: Check what raw_data we received
    print(f"\n--- Raw Data Preview ---")
    print(f"Length: {len(state['raw_data'])} characters")
    print(f"Preview: {state['raw_data'][:300]}...")

    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    system_prompt = """You are a data curator. Extract and structure the key information from the raw meme data.

Your job is to:
1. Extract the most important facts about the meme
2. Identify origin information
3. Note key examples or usage patterns
4. Collect all URLs mentioned

Return ONLY a valid JSON object with these keys (no markdown, no extra text):
{
    "name": "Official meme name",
    "about": "What this meme is (2-3 sentences)",
    "origin": "Where it came from and when (2-3 sentences)",
    "usage": "How it's typically used (2-3 sentences)",
    "sources": ["url1", "url2", ...]
}

Be concise and factual. Only include information that appears in the raw data.
IMPORTANT: Return ONLY the JSON object, nothing else."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Raw data:\n\n{state['raw_data']}")
    ]

    response = llm.invoke(messages)

    # Debug: Print what we received
    print(f"\n--- Curator received response ---")
    print(f"Type: {type(response.content)}")
    print(f"Content preview: {response.content[:200]}...")

    # Parse the JSON response
    try:
        # Clean up the response in case it has markdown code blocks
        content = response.content.strip()

        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        curated_data = json.loads(content)
        print(f"✓ Successfully parsed JSON")

    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parsing failed: {e}")
        print(f"Raw content: {response.content}")
        # If LLM doesn't return valid JSON, create a basic structure
        curated_data = {
            "name": state["meme_name"],
            "about": "Information unavailable",
            "origin": "Information unavailable",
            "usage": "Information unavailable",
            "sources": []
        }

    print(f"✓ Curated data for: {curated_data.get('name', 'Unknown')}")

    return {
        **state,
        "curated_data": curated_data,
        "sources": curated_data.get("sources", [])
    }


# =============================================================================
# 4. EXPLAINER AGENT - Creates final comprehensive explanation
# =============================================================================

def explainer_node(state: MemeResearchState) -> MemeResearchState:
    """
    Explainer Agent: Creates a comprehensive, engaging explanation
    """
    print("\n✍️  EXPLAINER: Generating final explanation...")

    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    curated = state["curated_data"]
    sociolect = state.get("sociolect", "gen-z")
    meme_name = state.get("meme_name", "")

    # Retrieve generation-specific language patterns from ChromaDB
    print(f"📚 Retrieving {sociolect} language patterns from ChromaDB...")
    language_context = context_manager.get_formatted_context(
        sociolect=sociolect,
        query=meme_name,
        n_results=8  # Get top 8 relevant language patterns
    )
    print(f"✓ Retrieved context for {sociolect}")

    # Tailor the explanation style based on the target generation
    sociolect_prompts = {
        "boomer": """You are explaining internet memes to Baby Boomers (born 1946-1964) who may not be familiar with internet culture.

Style guidelines:
- Use very clear, simple language with NO slang or internet jargon
- Make comparisons to traditional media (TV shows, newspapers, etc.)
- Explain every internet term you use
- Be patient and thorough - assume minimal internet culture knowledge
- Use formal but friendly tone
- Keep it concise (3-4 short paragraphs)

Your explanation should help someone who didn't grow up with the internet understand both WHAT the meme is and WHY it's popular.""",

        "gen-x": """You are explaining internet memes to Generation X (born 1965-1980) who understand technology but may not follow all internet trends.

Style guidelines:
- Use clear language, minimal slang
- You can reference 90s/2000s pop culture they'd know
- Explain internet-specific terms briefly
- Conversational but informative tone
- Keep it concise (3 short paragraphs)

Your explanation should help someone tech-savvy but not chronically online understand the meme's context and appeal.""",

        "millenial": """You are explaining internet memes to Millennials (born 1981-1996) who grew up with the internet and understand online culture.

Style guidelines:
- Use casual, friendly language
- You can use some internet terms without explanation
- Reference early internet culture (forums, early social media)
- Conversational, slightly humorous tone
- Keep it concise (2-3 paragraphs)

Your explanation should help someone familiar with internet culture understand this specific meme's nuances.""",

        "gen-z": """You are explaining internet memes to Gen Z (born 1997-2012) who are digital natives and very familiar with internet culture.

Style guidelines:
- Use casual, informal language
- Internet slang is fine - they'll understand it
- Be brief and to-the-point
- Can reference current internet trends and platforms
- Conversational, witty tone
- Keep it very concise (2 short paragraphs)

Your explanation should provide context and background they might not know about this specific meme."""
    }

    # Get the appropriate prompt or default to gen-z
    base_prompt = sociolect_prompts.get(sociolect, sociolect_prompts["gen-z"])

    system_prompt = f"""{base_prompt}

IMPORTANT - Language Style Context:
{language_context}

Use the language patterns above to inform your writing style. Incorporate appropriate keywords, phrases, and tone naturally into your explanation. Match the grammar and sentence structure typical of this generation.

Using the curated data provided:
1. Briefly introduce what the meme is and where it came from.
2. Explain what it means and how people use it.
3. Add a quick note on why people find it funny or relatable.

End with a "Sources" section in markdown format listing URLs used."""

    curated_text = f"""
Meme: {curated.get('name', 'Unknown')}

About: {curated.get('about', 'N/A')}

Origin: {curated.get('origin', 'N/A')}

Usage: {curated.get('usage', 'N/A')}

Sources: {', '.join(curated.get('sources', []))}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=curated_text)
    ]

    response = llm.invoke(messages)

    print("✓ Explanation generated")

    return {
        **state,
        "final_explanation": response.content
    }


# =============================================================================
# 5. BUILD THE LANGGRAPH WORKFLOW
# =============================================================================

def create_meme_research_graph():
    """
    Creates the LangGraph workflow: Researcher → Curator → Explainer
    """
    workflow = StateGraph(MemeResearchState)

    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("curator", curator_node)
    workflow.add_node("explainer", explainer_node)

    # Define edges (pipeline flow)
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "curator")
    workflow.add_edge("curator", "explainer")
    workflow.add_edge("explainer", END)

    # Compile the graph
    return workflow.compile()


# =============================================================================
# 6. MAIN EXECUTION
# =============================================================================


def main():
    """Main function to run the LangGraph pipeline"""
    print("\n" + "="*70)
    print("LANGGRAPH MEME RESEARCH PIPELINE")
    print("Researcher → Curator → Explainer")
    print("="*70)

    # Create the graph
    graph = create_meme_research_graph()

    while True:
        meme_name = input("\n\nWhat meme would you like to learn about? (or 'quit' to exit): ")

        if meme_name.lower() in ['quit', 'exit', 'q']:
            print("\nThanks for using the Meme Research Pipeline!")
            break

        if not meme_name.strip():
            continue

        print("\n" + "="*70)
        print(f"ANALYZING: {meme_name}")
        print("="*70)

        # Initialize state
        initial_state = {
            "meme_name": meme_name,
            "sociolect": "gen-z",  # Default to gen-z for CLI
            "raw_data": "",
            "curated_data": {},
            "final_explanation": "",
            "sources": []
        }

        # Run the pipeline
        try:
            final_state = graph.invoke(initial_state)

            # Display results
            print("\n\n" + "="*70)
            print("FINAL EXPLANATION")
            print("="*70)
            print(final_state["final_explanation"])
            print("\n" + "="*70)

            # Ask if user wants to save
            save = input("\nSave this explanation? (y/n): ")
            if save.lower() == 'y':
                filename = f"{meme_name.replace(' ', '_')}_explanation.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {final_state['curated_data'].get('name', meme_name)}\n\n")
                    f.write(final_state["final_explanation"])
                print(f"✅ Saved to {filename}")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    main()
