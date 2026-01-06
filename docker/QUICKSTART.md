# ChromaDB Docker Quick Start

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed

## Start ChromaDB

### Windows (PowerShell)
```powershell
# From project root
.\scripts\start_chromadb.ps1

# Or manually
docker-compose up -d chromadb
```

### Linux/Mac
```bash
# From project root
chmod +x scripts/start_chromadb.sh
./scripts/start_chromadb.sh

# Or manually
docker-compose up -d chromadb
```

## Verify ChromaDB is Running

```bash
# Check status
docker-compose ps

# Check health
curl http://localhost:8000/api/v1/heartbeat

# View logs
docker-compose logs -f chromadb
```

## Stop ChromaDB

```bash
docker-compose down
```

## Using ChromaDB in Applications

The Streamlit app and Jupyter notebook will automatically:
1. Try to connect to ChromaDB at `http://localhost:8000`
2. Fall back to local ChromaDB if server is unavailable
3. Use mock mode if ChromaDB is not available

No code changes needed - just start the Docker container!

