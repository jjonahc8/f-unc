# Sociolect-Aware Explanations Examples

This document demonstrates how the API tailors meme explanations based on the target generation.

## How It Works

The `sociolect` parameter in the `/explain/explanation` endpoint determines the explanation style:

1. **State Management**: Added `sociolect` field to `MemeResearchState` in [langgraph_pipeline.py](langgraph_pipeline.py#L29)
2. **Prompt Customization**: The `explainer_node` uses different prompts based on sociolect in [langgraph_pipeline.py](langgraph_pipeline.py#L159-L217)
3. **API Integration**: The API passes sociolect to the pipeline in [api.py](api.py#L102)

## Explanation Styles by Generation

### Boomer (Born 1946-1964)
**Characteristics:**
- Very simple, clear language
- Explains ALL internet/tech terms
- Uses traditional media comparisons (TV, newspapers)
- Patient and thorough
- Formal but friendly tone

**Example:** "The 'Stonks' meme is a humorous image that plays on the word 'stocks,' which refers to shares in a company that can be bought and sold..."

---

### Gen-X (Born 1965-1980)
**Characteristics:**
- Clear language, minimal slang
- Assumes basic tech literacy
- References 90s/2000s pop culture
- Brief internet term explanations
- Conversational but informative

**Example:** Uses moderate technical terms, references things they'd know from the early internet era.

---

### Millennial (Born 1981-1996)
**Characteristics:**
- Casual, friendly language
- Can use internet terms without explanation
- References early internet culture (forums, early social media)
- Conversational, slightly humorous
- Assumes online culture familiarity

**Example:** "This meme blew up on social media because it perfectly captures..."

---

### Gen-Z (Born 1997-2012)
**Characteristics:**
- Very casual, informal language
- Internet slang is acceptable
- Brief and to-the-point
- References current platforms and trends
- Witty, conversational tone

**Example:** "Alright, so let's dive into the 'Stonks' meme! This one kicked off back in 2017... This bad boy blew up because who doesn't love poking fun at the wild world of investing?"

## Live Comparison Test

Run the test script to see all four styles side-by-side:

```bash
python server/test_sociolects.py
```

This will fetch explanations for the same meme using all four sociolects, allowing you to compare the different styles.

## API Usage Examples

**For a Boomer:**
```bash
curl "http://localhost:8000/explain/explanation?topic=stonks&sociolect=boomer"
```

**For Gen-X:**
```bash
curl "http://localhost:8000/explain/explanation?topic=stonks&sociolect=gen-x"
```

**For a Millennial:**
```bash
curl "http://localhost:8000/explain/explanation?topic=stonks&sociolect=millenial"
```

**For Gen-Z:**
```bash
curl "http://localhost:8000/explain/explanation?topic=stonks&sociolect=gen-z"
```

## Technical Implementation

### 1. State Schema Update
```python
class MemeResearchState(TypedDict):
    meme_name: str
    sociolect: str  # NEW: Target generation
    raw_data: str
    curated_data: dict
    final_explanation: str
    sources: list[str]
```

### 2. Explainer Node Customization
The explainer node now includes a dictionary of prompts for each sociolect:
```python
sociolect_prompts = {
    "boomer": "Very simple language...",
    "gen-x": "Clear language...",
    "millenial": "Casual language...",
    "gen-z": "Informal language..."
}
```

### 3. API Integration
```python
initial_state = {
    "meme_name": topic,
    "sociolect": sociolect.value,  # Passes enum value
    ...
}
```

## Benefits

1. **Accessibility**: Makes meme culture accessible to all generations
2. **Tailored Learning**: People learn better when content matches their context
3. **Reduced Confusion**: No jargon overload for older generations, no condescension for younger ones
4. **Educational**: Bridges generational gaps in internet culture
