# MCP Reranker - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
cd servers/mcp-reranker
pip install -e .

# For advanced cross-encoder models
pip install -e ".[models]"
```

## Dependencies

Required:
- `mcp>=0.1.0` - MCP SDK
- `numpy` - For ranking computations

Optional:
- `sentence-transformers` - For cross-encoder models
- `torch` - Required for cross-encoder models

## Running the Server

```bash
python -m servers.mcp_reranker.src.server
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "rag-reranker": {
      "command": "python",
      "args": ["-m", "servers.mcp_reranker.src.server"]
    }
  }
}
```

## Available Tools

1. **rerank** - Rerank using cross-encoder model
2. **llm_rerank** - Rerank using LLM scoring
3. **fuse_rankings** - Combine multiple rankings (RRF)
4. **diversify** - Apply diversity filtering (MMR)

## Reranking Methods

### Cross-Encoder Reranking
Best for: Precision improvement
- Uses bi-encoder for relevance scoring
- More accurate than retrieval scores
- Relatively fast

### LLM Reranking
Best for: Maximum quality
- Uses LLM for relevance judgment
- Highest quality but slower
- Best for final top results

### Reciprocal Rank Fusion (RRF)
Best for: Combining multiple retrievers
- Merges results from different sources
- Robust and parameter-free
- Improves overall recall

### Diversity (MMR)
Best for: Reducing redundancy
- Maximizes relevance and diversity
- Prevents similar results
- Good for exploratory search

## Example Usage

### Basic Reranking

```json
{
  "query": "What is machine learning?",
  "documents": [
    {"id": "1", "text": "Machine learning is...", "score": 0.7},
    {"id": "2", "text": "AI includes...", "score": 0.6}
  ],
  "top_k": 5
}
```

### LLM Reranking

```json
{
  "query": "neural networks",
  "documents": [...],
  "model": "gpt-4"
}
```

### Fuse Multiple Rankings

```json
{
  "rankings": [
    [{"id": "1", "text": "..."}, {"id": "2", "text": "..."}],
    [{"id": "2", "text": "..."}, {"id": "3", "text": "..."}],
    [{"id": "1", "text": "..."}, {"id": "3", "text": "..."}]
  ],
  "k": 60
}
```

k parameter controls RRF weighting (higher = less weight on rank position)

### Apply Diversity

```json
{
  "documents": [...],
  "lambda_param": 0.7,
  "top_k": 10
}
```

Lambda parameter (0-1):
- 1.0 = pure relevance (no diversity)
- 0.5 = balanced
- 0.0 = pure diversity (no relevance)

## Typical RAG Pipeline

```
1. Retrieve (retriever) → Get top 100 results
2. Rerank (reranker) → Improve top 20
3. Diversify (reranker) → Select final 10
4. Generate (generator) → Create response
```

## Testing

```bash
pytest tests/test_server.py -v
pytest tests/test_tools.py -v

# Test specific method
pytest tests/test_tools.py::test_rerank -v
pytest tests/test_tools.py::test_diversity -v
```

## Performance Tips

1. **Rerank top-k only**: Don't rerank all retrieval results
2. **Use cross-encoder** for speed, LLM for quality
3. **Apply diversity last** after reranking
4. **Batch reranking** when possible

## Common Patterns

### Two-Stage Retrieval

```
retrieve(top_k=100) → rerank(top_k=10)
```

### Multi-Source Fusion

```
[
  dense_search(top_k=20),
  sparse_search(top_k=20),
  hybrid_search(top_k=20)
] → fuse_rankings() → rerank()
```

### Quality + Diversity

```
retrieve() → rerank(top_k=20) → diversify(top_k=10)
```

## Troubleshooting

**All scores similar**: Query may be too broad or documents too similar

**Poor reranking quality**: Try LLM reranking or adjust query

**Too slow**: Reduce number of documents to rerank

**Diversity too aggressive**: Increase lambda_param closer to 1.0

## Next Steps

- Review [README.md](README.md) for algorithm details
- Test different reranking strategies
- Integrate with retriever and generator
- Tune parameters for your use case
