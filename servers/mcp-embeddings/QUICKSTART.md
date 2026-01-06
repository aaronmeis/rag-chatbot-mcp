# MCP Embeddings - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
cd servers/mcp-embeddings
pip install -e .

# For OpenAI embeddings
pip install -e ".[openai]"

# For local models
pip install -e ".[local]"

# For all features
pip install -e ".[all]"
```

## Dependencies

Required:
- `mcp>=0.1.0` - MCP SDK
- `numpy` - For embedding operations

Optional:
- `openai>=1.0.0` - For OpenAI embeddings
- `sentence-transformers` - For local embedding models

## Running the Server

### With OpenAI

```bash
export OPENAI_API_KEY=your-api-key
export EMBEDDING_MODEL=text-embedding-3-small

python -m servers.mcp_embeddings.src.server
```

### With Local Models

```bash
export EMBEDDING_MODEL=all-MiniLM-L6-v2

python -m servers.mcp_embeddings.src.server
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "rag-embeddings": {
      "command": "python",
      "args": ["-m", "servers.mcp_embeddings.src.server"],
      "env": {
        "OPENAI_API_KEY": "your-key-here",
        "EMBEDDING_MODEL": "text-embedding-3-small"
      }
    }
  }
}
```

## Available Tools

1. **embed_text** - Generate embedding for single text
2. **embed_batch** - Batch embedding generation
3. **set_model** - Configure embedding model
4. **get_model_info** - Get current model details

## Supported Models

### OpenAI Models
- `text-embedding-3-small` (1536 dims) - Fast and cost-effective
- `text-embedding-3-large` (3072 dims) - Highest quality
- `text-embedding-ada-002` (1536 dims) - Legacy model

### Local Models
- `all-MiniLM-L6-v2` (384 dims) - Fast and lightweight
- `all-mpnet-base-v2` (768 dims) - Good balance
- `e5-large-v2` (1024 dims) - High quality

## Example Usage

### Single Text Embedding

```json
{
  "text": "This is a sample document",
  "model": "text-embedding-3-small"
}
```

### Batch Embedding

```json
{
  "texts": [
    "First document",
    "Second document",
    "Third document"
  ],
  "model": "all-MiniLM-L6-v2"
}
```

### Change Model

```json
{
  "model": "text-embedding-3-large"
}
```

## Testing

```bash
# Test with mock embeddings (no API key needed)
pytest tests/test_server.py -v

# Test with real OpenAI (requires API key)
export OPENAI_API_KEY=your-key
pytest tests/test_tools.py -v

# Test local models (requires sentence-transformers)
pytest tests/test_tools.py::test_local_embeddings -v
```

## Performance Tips

1. **Use batch embedding** for multiple texts (more efficient)
2. **Choose smaller models** for faster processing
3. **Enable caching** - embeddings are cached automatically
4. **Use local models** for offline/private deployments

## Troubleshooting

**OpenAI API errors**: Check your API key and rate limits

**Local model download issues**: Ensure internet connection for first-time model download

**Memory errors with large batches**: Reduce batch size or use smaller models

## Cost Optimization

For OpenAI embeddings:
- Use `text-embedding-3-small` for most use cases
- Batch process documents when possible
- Cache embeddings to avoid re-computing

## Next Steps

- Review [README.md](README.md) for detailed API reference
- Experiment with different models in tests
- Integrate with vectorstore and retriever servers
