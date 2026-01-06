# mcp-reranker

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Result reranking MCP server for improving retrieval quality.

## Overview

The `mcp-reranker` server provides tools for reranking search results to improve relevance and diversity.

## Features

- Cross-encoder reranking
- LLM-based scoring
- Reciprocal rank fusion
- Diversity filtering

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-reranker
source venv-reranker/bin/activate  # On Windows: venv-reranker\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: Real reranking models
pip install sentence-transformers torch anthropic
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional: Cross-encoder models and LLM providers
pip install sentence-transformers anthropic
```

## Tools

### rerank

Rerank results using cross-encoder model.

**Parameters:**
- `query` (string, required): Original query
- `documents` (array, required): Documents to rerank
- `top_k` (int, optional): Number of results to return

### llm_rerank

Rerank using LLM relevance scoring.

**Parameters:**
- `query` (string, required): Original query
- `documents` (array, required): Documents to rerank
- `model` (string, optional): LLM model to use

### fuse_rankings

Combine multiple result sets using RRF.

**Parameters:**
- `rankings` (array, required): Multiple ranked lists
- `k` (int, optional): RRF parameter

### diversify

Apply diversity filtering to results.

**Parameters:**
- `documents` (array, required): Documents to diversify
- `lambda_param` (float, optional): Diversity weight

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

# Test specific reranking methods
pytest tests/ -v -k "cross_encoder"
pytest tests/ -v -k "llm"
pytest tests/ -v -k "fusion"
```

### What Gets Tested

- ✅ Cross-encoder reranking
- ✅ LLM-based relevance scoring
- ✅ Reciprocal rank fusion (RRF)
- ✅ Diversity filtering
- ✅ Multiple ranking combination
- ✅ Score normalization
- ✅ Error handling
- ✅ Mock mode (without models)

**Note:** Tests work in mock mode without sentence-transformers or LLM APIs. Install them for real reranking.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide
