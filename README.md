# f(unc) - Meme Explainer 🧠

**AI-powered meme translation across generations.**

LangGraph-based system that uses Claude Sonnet to explain internet memes in generation-specific language (Boomer, Gen-X, Millennial, Gen-Z).

## 🤖 AI/ML Architecture

### LangGraph Multi-Agent Workflow

**3-Node Pipeline**:

1. **Scrape Agent** → BeautifulSoup4 extracts meme data from Know Your Meme
2. **Curate Agent** → Structures data, stores embeddings in ChromaDB
3. **Explain Agent** → Claude Sonnet generates sociolect-tailored explanations

```
User Input (meme_name, sociolect)
    ↓
[Scrape] → Raw HTML from KnowYourMeme
    ↓
[Curate] → Structured JSON + ChromaDB storage
    ↓
[Explain] → Claude Sonnet + Dynamic Prompts
    ↓
Output (meme_name, explanation)
```

### Prompt Engineering Strategy

**Dynamic System Prompts** - Each generation gets customized instructions:

- **Language Context Analysis**: Generation-specific vocabulary, grammar, cultural references
- **Tone Calibration**: Formal (Boomer) → Ultra-casual (Gen-Z)
- **Cultural Touchpoints**: Era-appropriate references (MTV for Gen-X, TikTok for Gen-Z)

**Examples**:
- **Gen-Z**: "Use internet slang. Reference TikTok, 'no cap', 'fr fr'. Keep it brief and lowercase."
- **Boomer**: "Write formally with complete sentences. Reference traditional media. Explain thoroughly."
- **Gen-X**: "Be skeptical and ironic. Reference MTV, 90s culture. Use dry humor."
- **Millennial**: "Reference social media, workplace culture. Use some emoji."

### Why LangGraph?

- **State Management**: Persists meme data across pipeline nodes
- **Error Handling**: Automatic retry logic for failed scrapes
- **Modularity**: Easy to extend with new nodes (e.g., image generation, fact-checking)
- **Observability**: Built-in logging and debugging

## 🛠️ Tech Stack

**AI/ML**: LangGraph, Langchain, Anthropic Claude Sonnet, ChromaDB  
**Backend**: FastAPI, Python 3.12+, BeautifulSoup4, YouTube Data API  
**Frontend**: Next.js 15, React 18, TypeScript, Tailwind CSS, Geist Mono

## 🚀 Quick Start

```bash
# Backend
pip install fastapi uvicorn langchain langchain-anthropic langgraph chromadb beautifulsoup4
python -m uvicorn server.api:app --reload --port 8000

# Frontend (in new terminal)
cd client && npm install && npm run dev
```

**Environment Variables**:
- `ANTHROPIC_API_KEY`: Claude API key
- `YOUTUBE_API_KEY`: YouTube Data API v3 key

## 🚢 Deploy to Vercel

### Frontend Deployment

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy from CLI**:
   ```bash
   cd client
   vercel
   ```

3. **Or deploy via GitHub**:
   - Push your code to GitHub
   - Visit [vercel.com](https://vercel.com)
   - Import your repository
   - Vercel auto-detects Next.js configuration
   - Add environment variable: `NEXT_PUBLIC_API_URL` (your backend URL)

### Backend Deployment Options

**Option 1: Railway/Render/Fly.io**
```bash
# Install dependencies and run
pip install -r requirements.txt
uvicorn server.api:app --host 0.0.0.0 --port $PORT
```

**Option 2: Docker**
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server/ ./server/
CMD ["uvicorn", "server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Environment Variables for Backend**:
- `ANTHROPIC_API_KEY`
- `YOUTUBE_API_KEY`

## 📁 Project Structure

```
server/
├── api.py                   # FastAPI endpoints
├── langgraph_pipeline.py    # 3-node LangGraph workflow
└── youtube_utils.py         # YouTube integration

client/
├── app/page.tsx             # Main UI with sliding transitions
├── components/              # LoadingDots, ResultsDisplay, VideoCollage
└── lib/                     # API client, TypeScript types
```

## 🧪 Pipeline Deep Dive

### Node 1: Scrape
**Input**: `meme_name` (string)  
**Process**: Searches Know Your Meme, extracts HTML  
**Output**: `raw_data` (HTML string)

### Node 2: Curate
**Input**: `raw_data`  
**Process**: Parses HTML → extracts name, about, origin, usage → stores in ChromaDB  
**Output**: `curated_data` (structured JSON)

### Node 3: Explain
**Input**: `curated_data`, `sociolect`  
**Process**:
1. Load sociolect-specific prompt template
2. Inject meme data into prompt
3. Call Claude Sonnet via Langchain
4. Parse and return explanation

**Output**: `final_explanation` (generation-tailored text)

### State Object

```python
{
    "meme_name": str,
    "sociolect": str,  # "boomer" | "gen-x" | "millenial" | "gen-z"
    "raw_data": str,
    "curated_data": dict,
    "final_explanation": str,
    "sources": list[str]
}
```

---

Built with 💚 to decode internet culture across generations.
