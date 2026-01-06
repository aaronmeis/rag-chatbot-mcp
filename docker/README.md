# Docker Setup for RAG Chatbot MCP Platform

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

This directory contains Docker configurations for running ChromaDB and other services.

## ChromaDB Docker Container

ChromaDB can be run in a Docker container to avoid local installation issues, especially on Windows.

### Quick Start

```bash
# Start ChromaDB
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f chromadb

# Stop ChromaDB
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### Using ChromaDB Client

The applications will automatically detect if ChromaDB is running in Docker and connect via HTTP.

**Connection Details:**
- Host: `localhost`
- Port: `8000`
- API: `http://localhost:8000`

### Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

**Data persistence:**
- Data is stored in a Docker volume named `chroma_data`
- To reset: `docker-compose down -v`

**Check if ChromaDB is running:**
```bash
curl http://localhost:8000/api/v1/heartbeat
```

### Integration

The Streamlit app and Jupyter notebook will automatically:
1. Try to connect to ChromaDB server at `http://localhost:8000`
2. Fall back to local ChromaDB if server is not available
3. Use mock mode if ChromaDB is not available at all

