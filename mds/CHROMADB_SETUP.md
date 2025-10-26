# ChromaDB Setup Guide

This project supports both **local** and **hosted** ChromaDB for storing generation-specific language patterns.

## Table of Contents
- [Local ChromaDB (Default)](#local-chromadb-default)
- [Hosted ChromaDB Setup](#hosted-chromadb-setup)
- [Configuration](#configuration)
- [Testing the Connection](#testing-the-connection)
- [Syncing Data](#syncing-data)

---

## Local ChromaDB (Default)

By default, the project uses **local ChromaDB** which stores data in the `./chroma_db` directory.

### Pros:
- No external dependencies
- Free
- Fast for development
- Data stored locally

### Cons:
- Not shared across environments
- Lost if directory is deleted
- Requires local disk space

**No configuration needed!** Just install the dependencies and run:

```bash
pip install -r server/requirements.txt
python -m server.langgraph_pipeline
```

---

## Hosted ChromaDB Setup

Hosted ChromaDB allows you to store language patterns in the cloud, enabling:
- Shared data across multiple environments
- Better scalability
- Persistent storage without local files

### Option 1: ChromaDB Cloud (Recommended)

1. **Sign up for ChromaDB Cloud**
   - Visit: https://www.trychroma.com/
   - Create an account
   - Create a new deployment

2. **Get your credentials**
   - Host: Your instance URL (e.g., `your-instance.chroma.dev`)
   - Port: Usually `8000` or `443`
   - API Key: From your ChromaDB dashboard
   - Tenant: Usually `default_tenant`
   - Database: Usually `default_database`

3. **Configure environment variables**
   - Edit `server/.env` and uncomment/fill in:
   ```bash
   CHROMA_HOST=your-instance.chroma.dev
   CHROMA_PORT=8000
   CHROMA_API_KEY=your-api-key-here
   CHROMA_TENANT=default_tenant
   CHROMA_DATABASE=default_database
   ```

### Option 2: Self-Hosted ChromaDB

If you want to run your own ChromaDB server:

1. **Run ChromaDB server with Docker**
   ```bash
   docker pull chromadb/chroma
   docker run -p 8000:8000 chromadb/chroma
   ```

2. **Configure environment variables**
   ```bash
   CHROMA_HOST=localhost
   CHROMA_PORT=8000
   # No API key needed for local Docker instance
   CHROMA_TENANT=default_tenant
   CHROMA_DATABASE=default_database
   ```

3. **For production deployment**
   - Use your server's IP or domain instead of `localhost`
   - Set up authentication (API key)
   - Configure HTTPS/SSL

---

## Configuration

### Environment Variables

Add these to `server/.env`:

```bash
# ChromaDB Configuration
CHROMA_HOST=your-instance.chroma.dev  # Or localhost for self-hosted
CHROMA_PORT=8000                       # Default port
CHROMA_API_KEY=your-api-key           # Optional for authentication
CHROMA_TENANT=default_tenant          # Tenant name
CHROMA_DATABASE=default_database      # Database name
```

### How it Works

The `SociolectContextManager` automatically detects hosted mode:

1. If `CHROMA_HOST` is set → uses hosted ChromaDB
2. If `CHROMA_HOST` is not set → uses local ChromaDB at `./chroma_db`

**Automatic fallback**: If hosted connection fails, it falls back to local ChromaDB.

---

## Testing the Connection

### Test ChromaDB Connection

```bash
# Test the sociolect context manager
python -m server.sociolect_context
```

You should see:
- `🌐 Connecting to hosted ChromaDB at ...` (if using hosted)
- `✅ Connected to hosted ChromaDB ...` (on success)
- `💾 Using local ChromaDB at ...` (if using local)

### Test Full Pipeline

```bash
# Run the full meme pipeline
python -m server.langgraph_pipeline
```

### Test via API

```bash
# Start the server
./server/start_server.sh

# Test endpoint
curl "http://localhost:8000/explain/explanation?topic=rizz&sociolect=gen-z"
```

---

## Syncing Data

### From Local to Hosted

If you've been using local ChromaDB and want to migrate to hosted:

1. **Export local data** (manual approach):
   ```python
   from server.sociolect_context import SociolectContextManager

   # Connect to local DB
   local_manager = SociolectContextManager(persist_directory="./chroma_db")

   # Get all patterns
   for sociolect in ["boomer", "gen-x", "millenial", "gen-z"]:
       patterns = local_manager.get_all_patterns(sociolect)
       print(f"{sociolect}: {len(patterns)} patterns")
   ```

2. **Set up hosted ChromaDB** in `.env`

3. **Re-seed the hosted database**:
   ```python
   from server.sociolect_context import SociolectContextManager, seed_sociolect_data

   # This will automatically use hosted ChromaDB if CHROMA_HOST is set
   manager = SociolectContextManager()

   # Seed with default data
   seed_sociolect_data(manager)
   ```

### From Hosted to Local

1. Comment out `CHROMA_HOST` in `.env`
2. Run the seeding script again
3. Data will be stored locally in `./chroma_db`

---

## Troubleshooting

### Connection Failed

**Error**: `Failed to connect to hosted ChromaDB`

**Solutions**:
1. Check your `CHROMA_HOST` is correct
2. Verify `CHROMA_API_KEY` is valid
3. Check firewall/network settings
4. Ensure ChromaDB server is running (for self-hosted)

### Authentication Failed

**Error**: `401 Unauthorized`

**Solutions**:
1. Verify your `CHROMA_API_KEY` is correct
2. Check API key hasn't expired
3. Ensure you're using the right tenant/database

### Collections Not Found

**Error**: `Collection not found`

**Solutions**:
1. Run the seed script: `python -m server.sociolect_context`
2. The collections will be auto-created on first use

---

## Best Practices

### Development
- Use **local ChromaDB** for development
- Fast iteration, no network dependencies

### Production
- Use **hosted ChromaDB** for production
- Shared data across servers
- Better reliability and scaling

### Data Management
- Keep seed data updated in `sociolect_context.py`
- Version control seed patterns
- Document custom patterns you add

---

## Adding Custom Language Patterns

You can add your own language patterns to the database:

```python
from server.sociolect_context import SociolectContextManager

manager = SociolectContextManager()

# Add custom patterns
custom_patterns = [
    {
        "text": "that slaps",
        "category": "phrase",
        "context": "showing strong approval"
    },
    {
        "text": "mid",
        "category": "keyword",
        "context": "mediocre or disappointing"
    }
]

manager.add_language_patterns("gen-z", custom_patterns)
```

---

## Support

For ChromaDB-specific issues:
- ChromaDB Docs: https://docs.trychroma.com/
- ChromaDB Discord: https://discord.gg/MMeYNTmh3x
- GitHub Issues: https://github.com/chroma-core/chroma

For this project:
- Check the code in `server/sociolect_context.py`
- Run test scripts to verify setup
