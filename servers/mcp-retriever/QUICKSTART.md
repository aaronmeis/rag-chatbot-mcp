# MCP Retriever - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
cd servers/mcp-retriever
pip install -e .
```

## Dependencies

Required:
- `mcp>=0.1.0` - MCP SDK
- `numpy` - For similarity computations

Optional:
- `requests` - For HTTP communication with other services

## Running the Server

### Local Development

```bash
python -m servers.mcp_retriever.src.server
```

### With Environment Variables

```bash
export VECTORSTORE_URL=http://localhost:8000
export EMBEDDINGS_URL=http://localhost:8001

python -m servers.mcp_retriever.src.server
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "rag-retriever": {
      "command": "python",
      "args": ["-m", "servers.mcp_retriever.src.server"],
      "env": {
        "VECTORSTORE_URL": "http://localhost:8000",
        "EMBEDDINGS_URL": "http://localhost:8001"
      }
    }
  }
}
```

## Available Tools

1. **retrieve** - Basic semantic search retrieval
2. **retrieve_with_filters** - Filtered retrieval with metadata
3. **hybrid_search** - Combined dense + sparse search
4. **multi_query_retrieve** - Query expansion for better recall
5. **set_retrieval_params** - Configure default parameters

## Example Usage

### Basic Retrieval

```json
{
  "query": "What is machine learning?",
  "collection": "my_documents",
  "top_k": 10
}
```

### Hybrid Search

```json
{
  "query": "neural networks",
  "collection": "my_documents",
  "alpha": 0.7,
  "top_k": 5
}
```

Alpha parameter (0-1):
- 1.0 = pure semantic (dense)
- 0.0 = pure keyword (sparse)
- 0.5 = balanced

### Multi-Query Retrieval

```json
{
  "query": "deep learning",
  "collection": "my_documents",
  "num_queries": 3,
  "top_k": 10
}
```

## Testing

```bash
pytest tests/test_server.py -v
pytest tests/test_tools.py -v
```

## Integration

The retriever typically works with:
- **mcp-vectorstore** - For document storage
- **mcp-embeddings** - For query embedding
- **mcp-reranker** - For result refinement

## Troubleshooting

**No results returned**: Check that vectorstore is populated and accessible

**Low quality results**: Try hybrid search or multi-query retrieval

**Connection errors**: Verify VECTORSTORE_URL and EMBEDDINGS_URL

## Next Steps

- Review [README.md](README.md) for advanced features
- Explore different search strategies in tests
- Integrate with vectorstore and embeddings servers
