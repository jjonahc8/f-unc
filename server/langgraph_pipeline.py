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
import json

load_dotenv()


# =============================================================================
# 1. DEFINE STATE SCHEMA
# =============================================================================

class MemeResearchState(TypedDict):
    """State that flows through the agent pipeline"""
    meme_name: str
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

    system_prompt = """You are a meme expert who explains internet culture to older adults in clear, simple language.

Your goal is to make the explanation short, easy to follow, and a little funny.
Avoid slang unless you're explaining it.
Keep the tone conversational —

Using the curated data provided:
1. Briefly introduce what the meme is and where it came from.
2. Explain what it means and how people use it.
3. Add a quick note on why people find it funny or relatable.

Keep it concise (under 3 short paragraphs). 
Avoid long sentences, complex words, or deep internet jargon.
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
