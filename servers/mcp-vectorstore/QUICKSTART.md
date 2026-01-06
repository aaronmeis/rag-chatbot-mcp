# MCP VectorStore - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
# From the server directory
cd servers/mcp-vectorstore
pip install -e .

# Or install with all dependencies
pip install -e ".[all]"
```

## Dependencies

Required:
- `chromadb>=0.4.0` - ChromaDB vector database
- `mcp>=0.1.0` - MCP SDK

Optional:
- `faiss-cpu` - For FAISS backend support
- `numpy` - For FAISS operations

## Running the Server

### Local Development (STDIO)

```bash
python -m servers.mcp_vectorstore.src.server
```

### With Environment Variables

```bash
# Set backend (chromadb or faiss)
export VECTORSTORE_BACKEND=chromadb
export VECTORSTORE_PATH=./my_vector_db

python -m servers.mcp_vectorstore.src.server
```

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rag-vectorstore": {
      "command": "python",
      "args": ["-m", "servers.mcp_vectorstore.src.server"],
      "env": {
        "VECTORSTORE_BACKEND": "chromadb",
        "VECTORSTORE_PATH": "./chroma_db"
      }
    }
  }
}
```

## Available Tools

1. **create_collection** - Create a new vector collection
2. **add_documents** - Add documents with embeddings
3. **search_similar** - Semantic similarity search
4. **delete_documents** - Remove documents by ID
5. **list_collections** - List all collections
6. **get_collection_stats** - Get collection statistics

## Example Usage

### Create a Collection

```json
{
  "name": "my_documents",
  "metadata": {"description": "My document collection"},
  "embedding_dimension": 1536
}
```

### Add Documents

```json
{
  "collection": "my_documents",
  "documents": ["Document 1 text", "Document 2 text"],
  "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
  "ids": ["doc1", "doc2"]
}
```

### Search

```json
{
  "collection": "my_documents",
  "query_embedding": [0.15, 0.25, ...],
  "top_k": 5
}
```

## Testing

```bash
# Run unit tests
pytest tests/test_server.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

**ChromaDB not available**: Install with `pip install chromadb`

**FAISS not working**: Install with `pip install faiss-cpu`

**Import errors**: Make sure you're running from the project root

## Next Steps

- See [README.md](README.md) for detailed documentation
- Check [tests/test_server.py](tests/test_server.py) for usage examples
- Review the [main servers README](../README.md) for integration patterns
