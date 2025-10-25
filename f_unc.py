"""
Meme Format Research Assistant
A LangChain-powered agent that searches for specific meme formats and explains their meaning
Combines multi-agent system with LangChain for structured research
"""

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_knowyourmeme, explain_meme_format, save_meme_explanation

load_dotenv()


class BrainrotExplanation(BaseModel):
    """Structured response for meme format explanations"""
    meme_name: str
    format_description: str
    origin: str
    typical_usage: str
    cultural_context: str
    sources: list[str]
    tools_used: list[str]


# Initialize OpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
parser = PydanticOutputParser(pydantic_object=BrainrotExplanation)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a meme culture expert and research assistant.

            When a user asks about ANY meme:
            1. Use search_knowyourmeme to find information from knowyourmeme.com
               (This provides About and Origin sections from the official Know Your Meme database)
            2. Use explain_meme_format to generate a comprehensive AI explanation based on the KYM data
            3. Synthesize all information into a clear, structured response

            Your goal is to help users understand:
            - What the meme format looks like (template/structure)
            - Where it originated (source, date, original context)
            - How it's typically used (message, tone, variations)
            - Why it's funny or meaningful (cultural relevance)
            - Cultural context and current relevance

            Wrap the output in this format and provide no other text:
            {format_instructions}

            Be thorough and use the tools to gather complete information.
            Always cite your sources (Know Your Meme URLs).
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Set up tools and agent
tools = [search_knowyourmeme, explain_meme_format, save_meme_explanation]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=6
)


def main():
    """Main function to run the meme research assistant"""
    print("\n" + "="*70)
    print("MEME FORMAT RESEARCH ASSISTANT")
    print("Powered by LangChain + OpenAI + Reddit + Wikipedia")
    print("="*70)
    print("\nExamples: 'drake meme', 'distracted boyfriend', 'Huzz meme', 'NPC meme'")
    print("Type 'quit' to exit\n")

    while True:
        query = input("\nWhat meme would you like to learn about? ")

        if query.lower() in ['quit', 'exit', 'q']:
            print("\nThanks for using the Meme Research Assistant!")
            break

        if not query.strip():
            continue

        print("\n" + "-"*70)
        print(f"Researching: {query}")
        print("-"*70 + "\n")

        try:
            # Run the agent
            raw_response = agent_executor.invoke({"query": query})

            # Try to parse structured response
            try:
                # The output is in raw_response['output']
                output_text = raw_response.get("output", "")
                structured_response = parser.parse(output_text)

                print("\n" + "="*70)
                print("Brainrot EXPLANATION")
                print("="*70)
                print(f"\n📛 Brainrot: {structured_response.meme_name}")
                print(f"\n🎨 Format: {structured_response.format_description}")
                print(f"\n📜 Origin: {structured_response.origin}")
                print(f"\n💬 Typical Usage: {structured_response.typical_usage}")
                print(f"\n🌍 Cultural Context: {structured_response.cultural_context}")
                print(f"\n🔗 Sources: {', '.join(structured_response.sources)}")
                print(f"\n🛠️  Tools Used: {', '.join(structured_response.tools_used)}")
                print("\n" + "="*70)

                # Ask if user wants to save
                save = input("\nWould you like to save this explanation? (y/n): ")
                if save.lower() == 'y':
                    filename = f"{structured_response.meme_name.replace(' ', '_')}_explanation.txt"
                    content = f"""MEME EXPLANATION: {structured_response.meme_name}

FORMAT DESCRIPTION:
{structured_response.format_description}

ORIGIN:
{structured_response.origin}

TYPICAL USAGE:
{structured_response.typical_usage}

CULTURAL CONTEXT:
{structured_response.cultural_context}

SOURCES:
{', '.join(structured_response.sources)}

Generated by Meme Format Research Assistant
"""
                    save_meme_explanation.invoke({"content": content, "filename": filename})
                    print(f"✅ Saved to {filename}")

            except Exception as parse_error:
                print("\n" + "="*70)
                print("RAW RESPONSE (Structured parsing not available)")
                print("="*70)
                print(f"\nNote: {parse_error}")
                print(f"\nAgent's Response:\n{raw_response.get('output', 'No output')}")
                print("\n" + "="*70)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    main()
