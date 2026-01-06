# mcp-chunker

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Document chunking MCP server for text preprocessing.

## Overview

The `mcp-chunker` server provides tools for splitting documents into optimal chunks for RAG pipelines, with various chunking strategies.

## Features

- Multiple chunking strategies
- Configurable chunk sizes
- Overlap control
- Metadata preservation

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-chunker
source venv-chunker/bin/activate  # On Windows: venv-chunker\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: Advanced chunking with NLP
pip install spacy nltk
python -m spacy download en_core_web_sm
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional: NLP-based chunking
pip install spacy nltk
```

## Tools

### chunk_text

Split text using specified strategy.

**Parameters:**
- `text` (string, required): Text to chunk
- `strategy` (string, optional): Chunking strategy
- `chunk_size` (int, optional): Target chunk size
- `overlap` (int, optional): Overlap between chunks

### chunk_document

Process entire document with metadata.

**Parameters:**
- `document` (object, required): Document with text and metadata
- `strategy` (string, optional): Chunking strategy

### set_chunk_size

Configure default chunk size.

**Parameters:**
- `size` (int, required): Chunk size in characters/tokens

### set_overlap

Configure chunk overlap.

**Parameters:**
- `overlap` (int, required): Overlap size

### preview_chunks

Preview chunking without saving.

**Parameters:**
- `text` (string, required): Text to preview
- `strategy` (string, optional): Strategy to use

## Chunking Strategies

| Strategy | Description |
|----------|-------------|
| `fixed` | Fixed character count |
| `recursive` | Split by separators |
| `semantic` | Split by meaning |
| `sentence` | Split by sentences |
| `paragraph` | Split by paragraphs |

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

# Test specific strategies
pytest tests/ -v -k "fixed"
pytest tests/ -v -k "recursive"
pytest tests/ -v -k "semantic"
```

### What Gets Tested

- ✅ Fixed-size chunking
- ✅ Recursive chunking (by separators)
- ✅ Semantic chunking
- ✅ Sentence-based chunking
- ✅ Paragraph-based chunking
- ✅ Chunk overlap configuration
- ✅ Metadata preservation
- ✅ Chunk preview functionality
- ✅ Error handling

**Note:** Tests work in mock mode without spacy/nltk. Install them for NLP-based chunking.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide
