# mcp-retriever

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Document retrieval MCP server with multiple search strategies.

## Overview

The `mcp-retriever` server provides tools for finding relevant documents using dense (semantic), sparse (keyword), and hybrid search methods.

## Features

- Dense retrieval (vector similarity)
- Sparse retrieval (BM25)
- Hybrid search combining both
- Metadata filtering
- Query expansion

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-retriever
source venv-retriever/bin/activate  # On Windows: venv-retriever\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: Full retrieval functionality
pip install rank-bm25 numpy
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional dependencies for full functionality
pip install rank-bm25
```

## Tools

### retrieve

Basic retrieval with top-k results.

**Parameters:**
- `query` (string, required): Search query
- `collection` (string, required): Collection to search
- `top_k` (int, optional): Number of results (default: 10)

### retrieve_with_filters

Retrieval with metadata filtering.

**Parameters:**
- `query` (string, required): Search query
- `collection` (string, required): Collection to search
- `filters` (object, required): Metadata filters
- `top_k` (int, optional): Number of results

### hybrid_search

Combined dense + sparse search.

**Parameters:**
- `query` (string, required): Search query
- `collection` (string, required): Collection to search
- `alpha` (float, optional): Weight for dense vs sparse (0-1)
- `top_k` (int, optional): Number of results

### multi_query_retrieve

Query expansion retrieval.

**Parameters:**
- `query` (string, required): Original query
- `collection` (string, required): Collection to search
- `num_queries` (int, optional): Number of query variants

### set_retrieval_params

Configure retrieval parameters.

**Parameters:**
- `default_top_k` (int, optional): Default result count
- `similarity_threshold` (float, optional): Minimum similarity score

## Testing

### Quick Test

```bash
# From server directory
pytest tests/ -v
```

### Comprehensive Testing

```bash
# With coverage
pytest tests/ -v --cov=src --cov-report=html

# Specific test file
pytest tests/test_server.py -v
pytest tests/test_tools.py -v

# Test dense retrieval only
pytest tests/ -v -k "dense"

# Test hybrid search
pytest tests/ -v -k "hybrid"
```

### What Gets Tested

- ✅ Dense retrieval (vector similarity search)
- ✅ Sparse retrieval (BM25 keyword search)
- ✅ Hybrid search (combined dense + sparse)
- ✅ Metadata filtering
- ✅ Query expansion
- ✅ Multi-query retrieval
- ✅ Retrieval parameter configuration
- ✅ Error handling

**Note:** Tests work in mock mode without rank-bm25. Install it for real BM25 search.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide
