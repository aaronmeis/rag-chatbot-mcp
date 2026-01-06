# mcp-vectorstore

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Vector database operations MCP server for storing and searching embeddings.

## Overview

The `mcp-vectorstore` server provides tools for managing vector databases, including creating collections, adding documents with embeddings, and performing similarity searches.

## Features

- Multiple backend support (ChromaDB, FAISS)
- Metadata filtering
- Batch operations
- Collection management
- Persistence support

## Installation

```bash
pip install chromadb faiss-cpu numpy
```

## Tools

### create_collection

Create a new vector collection.

**Parameters:**
- `name` (string, required): Collection name
- `metadata` (object, optional): Collection metadata
- `embedding_dimension` (int, optional): Vector dimension (default: 1536)

**Example:**
```json
{
  "name": "create_collection",
  "arguments": {
    "name": "my_documents",
    "embedding_dimension": 1536
  }
}
```

### add_documents

Add documents with embeddings to a collection.

**Parameters:**
- `collection` (string, required): Collection name
- `documents` (array, required): Document texts
- `embeddings` (array, required): Document embeddings
- `metadatas` (array, optional): Document metadata
- `ids` (array, optional): Document IDs

**Example:**
```json
{
  "name": "add_documents",
  "arguments": {
    "collection": "my_documents",
    "documents": ["Document 1 text", "Document 2 text"],
    "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
    "metadatas": [{"source": "file1.pdf"}, {"source": "file2.pdf"}]
  }
}
```

### search_similar

Find similar documents by embedding.

**Parameters:**
- `collection` (string, required): Collection name
- `query_embedding` (array, required): Query vector
- `top_k` (int, optional): Number of results (default: 10)
- `filter` (object, optional): Metadata filter

**Example:**
```json
{
  "name": "search_similar",
  "arguments": {
    "collection": "my_documents",
    "query_embedding": [0.1, 0.2, ...],
    "top_k": 5
  }
}
```

### delete_documents

Remove documents from a collection.

**Parameters:**
- `collection` (string, required): Collection name
- `ids` (array, required): Document IDs to delete

### list_collections

List all available collections.

**Parameters:** None

### get_collection_stats

Get statistics for a collection.

**Parameters:**
- `collection` (string, required): Collection name

## Configuration

Environment variables:
- `VECTORSTORE_BACKEND`: Backend type (`chromadb` or `faiss`)
- `VECTORSTORE_PATH`: Persistence directory
- `VECTORSTORE_HOST`: Remote host (optional)

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-vectorstore
source venv-vectorstore/bin/activate  # On Windows: venv-vectorstore\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: Real vector database backends
pip install chromadb faiss-cpu
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional: Real backends
pip install chromadb faiss-cpu
```

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

# Test with real ChromaDB
pytest tests/ -v -m "not requires_faiss"

# Test all backends
pip install chromadb faiss-cpu
pytest tests/ -v
```

### What Gets Tested

- ✅ Collection creation and management
- ✅ Document addition with embeddings
- ✅ Similarity search (cosine, L2)
- ✅ Metadata filtering
- ✅ Document deletion
- ✅ Batch operations
- ✅ Multiple backends (ChromaDB, FAISS, mock)

**Note:** Tests work in mock mode (in-memory) without ChromaDB/FAISS. Install them for real database testing.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide

## See Also

- [mcp-embeddings](../mcp-embeddings/README.md) - Generate embeddings
- [mcp-retriever](../mcp-retriever/README.md) - Document retrieval
