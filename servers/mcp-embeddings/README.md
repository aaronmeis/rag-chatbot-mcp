# mcp-embeddings

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Embedding generation MCP server for converting text to vectors.

## Overview

The `mcp-embeddings` server provides tools for generating embeddings using various models, including OpenAI's text-embedding models and local sentence transformers.

## Features

- Multiple embedding model support
- Batch processing for efficiency
- Caching for repeated queries
- Local and API-based models

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-embeddings
source venv-embeddings/bin/activate  # On Windows: venv-embeddings\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: Full embeddings functionality
pip install openai sentence-transformers torch
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional: Real embedding providers
pip install openai sentence-transformers torch
```

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (for OpenAI models)
- `EMBEDDING_MODEL`: Default model to use
- `EMBEDDING_CACHE_DIR`: Cache directory for embeddings

## Tools

### embed_text

Generate embedding for a single text.

**Parameters:**
- `text` (string, required): Text to embed
- `model` (string, optional): Model to use

**Example:**
```json
{
  "name": "embed_text",
  "arguments": {
    "text": "What is machine learning?",
    "model": "text-embedding-3-small"
  }
}
```

### embed_batch

Generate embeddings for multiple texts.

**Parameters:**
- `texts` (array, required): List of texts to embed
- `model` (string, optional): Model to use

### set_model

Configure the default embedding model.

**Parameters:**
- `model` (string, required): Model name
- `provider` (string, optional): Provider (openai, local)

### get_model_info

Get information about current model configuration.

## Supported Models

| Model | Dimensions | Provider | Cost |
|-------|------------|----------|------|
| text-embedding-3-small | 1536 | OpenAI | $0.00002/1K |
| text-embedding-3-large | 3072 | OpenAI | $0.00013/1K |
| all-MiniLM-L6-v2 | 384 | Local | Free |
| all-mpnet-base-v2 | 768 | Local | Free |

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

# Test with real OpenAI embeddings (requires API key)
export OPENAI_API_KEY=your_key_here
pytest tests/ -v -m "not slow"

# Test with local models
pip install sentence-transformers torch
pytest tests/ -v
```

### What Gets Tested

- ✅ Text embedding (single and batch)
- ✅ Multiple model support (OpenAI, local transformers)
- ✅ Dimension validation
- ✅ Caching functionality
- ✅ Model configuration
- ✅ Error handling
- ✅ Mock mode (without API keys)

**Note:** Tests work in mock mode without OpenAI API key or local models. Install them for real embedding generation.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide
