# MCP Servers

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Overview

This directory contains 7 MCP servers that implement a complete RAG (Retrieval-Augmented Generation) pipeline. Each server is a standalone Python package that can be deployed independently.

## Server Status

| Server | Tools | Status | Coverage | Description |
|--------|-------|--------|----------|-------------|
| [mcp-vectorstore](mcp-vectorstore/) | 6 | ✅ Production | 85% | Vector database operations |
| [mcp-retriever](mcp-retriever/) | 5 | ✅ Production | 82% | Document retrieval |
| [mcp-embeddings](mcp-embeddings/) | 4 | ✅ Production | 88% | Embedding generation |
| [mcp-chunker](mcp-chunker/) | 5 | ✅ Production | 80% | Document chunking |
| [mcp-reranker](mcp-reranker/) | 4 | ✅ Production | 78% | Result reranking |
| [mcp-generator](mcp-generator/) | 5 | ✅ Production | 75% | Response generation |
| [mcp-datasources](mcp-datasources/) | 6 | ✅ Production | 83% | Data source connectors |

**Total: 35 tools across 7 servers**

## Quick Start

### Choose Your Setup Approach

**For Individual Server Development:**
```bash
# See ENVIRONMENT_GUIDE.md for detailed instructions
cd servers/mcp-vectorstore
python -m venv venv-vectorstore
source venv-vectorstore/bin/activate
pip install -e .
pip install -r ../test-requirements.txt
pytest tests/ -v
```

**For End-to-End Testing (All Servers):**
```bash
# See ENVIRONMENT_GUIDE.md for detailed instructions
cd servers/
python -m venv venv-shared
source venv-shared/bin/activate
pip install -e mcp-*/
pip install -r test-requirements.txt
./run_all_tests.sh -v
```

**Quick Setup with Script:**
```bash
cd servers/
./setup_tests.sh  # Interactive setup wizard
```

### Configure Claude Desktop

Copy the configuration file:
```bash
cp ../desktop-configs/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

## Server Details

### mcp-vectorstore
Vector database operations for storing and searching embeddings.

**Tools:**
- `create_collection` - Create a new vector collection
- `add_documents` - Add documents with embeddings to collection
- `search_similar` - Find similar documents by embedding
- `delete_documents` - Remove documents from collection
- `list_collections` - List all collections
- `get_collection_stats` - Get collection statistics

### mcp-retriever
Document retrieval with multiple search strategies.

**Tools:**
- `retrieve` - Basic retrieval with top-k results
- `retrieve_with_filters` - Retrieval with metadata filtering
- `hybrid_search` - Combined dense + sparse search
- `multi_query_retrieve` - Query expansion retrieval
- `set_retrieval_params` - Configure retrieval parameters

### mcp-embeddings
Generate embeddings using various models.

**Tools:**
- `embed_text` - Generate embedding for single text
- `embed_batch` - Batch embedding generation
- `set_model` - Configure embedding model
- `get_model_info` - Get current model information

### mcp-chunker
Document chunking and preprocessing.

**Tools:**
- `chunk_text` - Split text using specified strategy
- `chunk_document` - Process document with metadata
- `set_chunk_size` - Configure chunk size
- `set_overlap` - Configure chunk overlap
- `preview_chunks` - Preview without saving

### mcp-reranker
Rerank and filter retrieval results.

**Tools:**
- `rerank` - Rerank using cross-encoder
- `llm_rerank` - Rerank using LLM scoring
- `fuse_rankings` - Combine multiple rankings
- `diversify` - Apply diversity filtering

### mcp-generator
Generate responses from context.

**Tools:**
- `generate_response` - Generate answer from context
- `summarize_context` - Summarize documents
- `extract_info` - Extract structured information
- `generate_with_citations` - Generate with citations
- `set_prompt_template` - Configure prompt template

### mcp-datasources
Load data from various sources.

**Tools:**
- `load_files` - Load from filesystem
- `load_url` - Fetch web content
- `load_api` - Query REST APIs
- `load_database` - Query databases
- `list_sources` - List data sources
- `get_source_info` - Get source metadata

## Development

### Server Structure

Each server follows this structure:
```
mcp-{name}/
├── README.md           # Server documentation
├── QUICKSTART.md       # Quick start guide
├── pyproject.toml      # Package configuration
├── src/
│   ├── __init__.py
│   ├── server.py       # MCP server implementation
│   ├── tools.py        # Tool implementations
│   └── utils.py        # Utility functions
└── tests/
    ├── __init__.py
    ├── test_server.py  # Server tests
    └── test_tools.py   # Tool tests
```

### Running Tests

**Individual Server (Isolated Environment):**
```bash
cd servers/mcp-vectorstore
source venv-vectorstore/bin/activate
pytest tests/ -v
```

**All Servers (Shared Environment):**
```bash
cd servers/
source venv-shared/bin/activate
./run_all_tests.sh -v
```

**See Also:**
- [ENVIRONMENT_GUIDE.md](ENVIRONMENT_GUIDE.md) - Environment management strategy
- [TEST_GUIDE.md](TEST_GUIDE.md) - Comprehensive testing guide
- [QUICK_TEST_SETUP.md](QUICK_TEST_SETUP.md) - Fast setup guide

### Adding New Tools

1. Define the tool in `src/tools.py`
2. Register it in `src/server.py`
3. Add tests in `tests/test_tools.py`
4. Update documentation

## Deployment

### Local (STDIO)
```json
{
  "mcpServers": {
    "rag-vectorstore": {
      "command": "python",
      "args": ["-m", "servers.mcp_vectorstore.src.server"]
    }
  }
}
```

### Cloud (SSE/HTTP)
```bash
# Deploy to Cloud Run
cd infrastructure/gcp
./deploy.sh mcp-vectorstore
```

## Testing Documentation

- [ENVIRONMENT_GUIDE.md](ENVIRONMENT_GUIDE.md) - **Environment management strategy** (separate vs shared)
- [QUICK_TEST_SETUP.md](QUICK_TEST_SETUP.md) - 2-minute quick start
- [TEST_GUIDE.md](TEST_GUIDE.md) - Comprehensive testing guide
- [TESTING_README.md](TESTING_README.md) - Testing infrastructure overview
- [TESTING_SUMMARY.md](TESTING_SUMMARY.md) - Implementation details

## See Also

- [Architecture Overview](../architecture/README.md)
- [RAG Pipeline](../architecture/rag-pipeline/README.md)
- Individual server READMEs for server-specific documentation
