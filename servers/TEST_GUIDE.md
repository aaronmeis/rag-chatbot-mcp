# MCP Servers Testing Guide

This guide explains how to run tests for each MCP server independently.

## Quick Start

### Run Tests for a Specific Server

```bash
# Navigate to a server directory
cd servers/mcp-vectorstore

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_server.py -v
pytest tests/test_tools.py -v
```

### Run Tests for All Servers

```bash
# From the servers directory
cd servers

# Run all server tests
pytest */tests/ -v

# Run with detailed output
pytest */tests/ -v -s
```

## Test Structure

Each server has the following test files:

```
mcp-{server}/
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── conftest.py          # Shared fixtures and mock data
│   ├── test_server.py       # Server integration tests
│   └── test_tools.py        # Tool-specific unit tests
```

### conftest.py
Contains:
- **Fixtures**: Reusable test data and server instances
- **Mock Data**: Sample documents, embeddings, queries, etc.
- **Setup/Teardown**: Test environment configuration

### test_server.py
Tests:
- Complete workflows from start to finish
- Server manager class functionality
- Integration between components
- Error handling and edge cases

### test_tools.py
Tests:
- Individual tool functions
- Input validation
- Output formats
- Edge cases and error conditions

## Running Individual Server Tests

### mcp-vectorstore

```bash
cd servers/mcp-vectorstore
pytest tests/ -v
```

**What it tests:**
- Collection creation and management
- Document addition with embeddings
- Similarity search
- Document deletion
- Collection statistics

**Mock data:**
- Sample embeddings (1536 dimensions)
- Sample documents about ML/AI
- Metadata with sources and topics

### mcp-retriever

```bash
cd servers/mcp-retriever
pytest tests/ -v
```

**What it tests:**
- Basic semantic retrieval
- Filtered retrieval with metadata
- Hybrid search (dense + sparse)
- Multi-query retrieval
- Parameter configuration

**Mock data:**
- Sample queries about ML
- Mock search results with scores
- Metadata filters

### mcp-embeddings

```bash
cd servers/mcp-embeddings
pytest tests/ -v
```

**What it tests:**
- Single text embedding
- Batch embedding generation
- Model switching
- Embedding caching
- Dimension validation

**Mock data:**
- Sample texts for embedding
- Long texts for limit testing
- Expected dimensions for each model

### mcp-chunker

```bash
cd servers/mcp-chunker
pytest tests/ -v
```

**What it tests:**
- Fixed-size chunking
- Recursive chunking
- Sentence-based chunking
- Paragraph splitting
- Metadata preservation

**Mock data:**
- Short and long sample texts
- Documents with metadata
- Text with clear paragraph boundaries

### mcp-reranker

```bash
cd servers/mcp-reranker
pytest tests/ -v
```

**What it tests:**
- Cross-encoder reranking
- LLM-based reranking
- Reciprocal rank fusion (RRF)
- MMR diversity filtering

**Mock data:**
- Documents with relevance scores
- Multiple rankings for fusion
- Diverse documents for MMR testing

### mcp-generator

```bash
cd servers/mcp-generator
pytest tests/ -v
```

**What it tests:**
- Response generation from context
- Context summarization
- Structured information extraction
- Citation generation
- Template management

**Mock data:**
- Context documents with metadata
- Sample queries
- Extraction schemas
- Custom templates

### mcp-datasources

```bash
cd servers/mcp-datasources
pytest tests/ -v
```

**What it tests:**
- File loading (txt, md, json, csv)
- Directory traversal (recursive/non-recursive)
- URL fetching (mock)
- API querying (mock)
- Database loading (mock)

**Mock data:**
- Temporary test files
- Sample URLs and API endpoints
- Mock connection strings

## Test Requirements

### Required Packages

```bash
pip install pytest pytest-asyncio pytest-cov
```

### Optional Packages for Full Testing

```bash
# For vector store tests
pip install chromadb faiss-cpu

# For embeddings tests
pip install openai sentence-transformers

# For datasources tests
pip install beautifulsoup4 PyPDF2
```

## Running Tests Without Optional Dependencies

All tests are designed to work in "mock mode" without optional dependencies. They will:
- Use mock implementations when libraries aren't available
- Return synthetic data for testing
- Still validate business logic and data flow

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Run only integration tests
pytest -v -m integration

# Run only unit tests
pytest -v -m unit

# Skip slow tests
pytest -v -m "not slow"
```

## Debugging Tests

### Run with verbose output

```bash
pytest tests/ -v -s
```

### Run specific test

```bash
pytest tests/test_server.py::TestClass::test_method -v
```

### Run with debugger

```bash
pytest tests/ --pdb
```

### Show all test output

```bash
pytest tests/ -v -s --tb=short
```

## Coverage Reports

### Generate HTML coverage report

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html  # View in browser
```

### Show coverage in terminal

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## Continuous Integration

Tests can be run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd servers/mcp-vectorstore
    pytest tests/ -v --cov=src
```

## Troubleshooting

### Import Errors

If you see import errors:

```bash
# Add parent directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

Or run from server directory:

```bash
cd servers/mcp-vectorstore
pytest tests/ -v
```

### Fixture Not Found

Make sure `conftest.py` exists in the `tests/` directory. Pytest automatically discovers fixtures from this file.

### Tests Pass but Warning About Imports

This is normal - tests verify the logic works even in mock mode without all dependencies installed.

## Best Practices

1. **Run tests before committing**
   ```bash
   pytest tests/ -v
   ```

2. **Write new tests for new features**
   - Add test cases to `test_tools.py`
   - Add integration tests to `test_server.py`

3. **Update fixtures when changing data structures**
   - Modify `conftest.py`
   - Ensure all tests still pass

4. **Use descriptive test names**
   - `test_embed_text_returns_correct_dimensions`
   - `test_retrieval_with_empty_query`

5. **Test both success and failure cases**
   - Valid inputs → success
   - Invalid inputs → appropriate errors

## Next Steps

- Review individual server README.md files
- Check QUICKSTART.md for server-specific setup
- Read the main [servers/README.md](README.md) for architecture overview
