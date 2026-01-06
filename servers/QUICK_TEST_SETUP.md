# Quick Test Setup Guide

## TL;DR - Get Testing in 2 Minutes

```bash
# 1. Install essentials (required for all tests)
cd servers
pip install -r test-requirements.txt

# 2. Run tests (they work in mock mode without optional deps!)
cd mcp-vectorstore
pytest tests/ -v

# 3. (Optional) Install full dependencies for real implementations
pip install -r ../test-requirements-optional.txt
```

## Prerequisites

### Essential (Required) ✅

These are needed for **any** testing:

```bash
pip install -r test-requirements.txt
```

Installs:
- `pytest`, `pytest-asyncio`, `pytest-cov` - Test framework
- `mcp` - MCP SDK (required)
- `numpy` - Common utility

**Tests will run in mock mode without anything else!**

### Optional (Enhanced) 🎯

For full functionality with real implementations:

```bash
pip install -r test-requirements-optional.txt
```

Or pick what you need:

```bash
# Vectorstore: Real ChromaDB/FAISS backends
pip install chromadb faiss-cpu

# Embeddings: Real OpenAI/local models
pip install openai sentence-transformers torch

# Datasources: Real PDF/DOCX parsing
pip install beautifulsoup4 PyPDF2 python-docx pandas
```

## Three Ways to Setup

### Method 1: Interactive Setup (Easiest)

```bash
cd servers
./setup_tests.sh

# Follow prompts:
# 1 = Essential only (tests work in mock mode)
# 2 = Full install (all features)
# 3 = Custom (pick specific servers)
```

### Method 2: Quick Manual

```bash
# Essential only
pip install -r servers/test-requirements.txt

# Essential + everything
pip install -r servers/test-requirements.txt
pip install -r servers/test-requirements-optional.txt
```

### Method 3: Per-Server

```bash
# Just testing vectorstore?
pip install pytest pytest-asyncio mcp chromadb

# Just testing embeddings?
pip install pytest pytest-asyncio mcp openai
```

## What Works Without Optional Dependencies?

**Everything!** Tests are designed to run in "mock mode":

| Server | Without Optional Deps | With Optional Deps |
|--------|----------------------|-------------------|
| vectorstore | ✅ Mock in-memory storage | ✅ Real ChromaDB/FAISS |
| embeddings | ✅ Mock random vectors | ✅ Real OpenAI/local models |
| retriever | ✅ Mock similarity | ✅ Full search algorithms |
| chunker | ✅ All features work | ✅ Same (no extra deps needed) |
| reranker | ✅ All features work | ✅ Same (no extra deps needed) |
| generator | ✅ Mock generation | ✅ Real LLM calls |
| datasources | ✅ Mock file loading | ✅ Real PDF/DOCX parsing |

## Running Tests

### Single Server

```bash
cd servers/mcp-vectorstore
pytest tests/ -v
```

### All Servers

```bash
cd servers
./run_all_tests.sh -v
```

### With Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Only Tests That Don't Need Optional Deps

```bash
pytest tests/ -v -m "not requires_chromadb and not requires_openai"
```

## Verifying Your Setup

```bash
# Check what's installed
pip list | grep -E "pytest|mcp|chromadb|openai"

# See which tests will be skipped
pytest tests/ --collect-only -q

# Run with dependency info
pytest tests/ -v --tb=short
```

## Common Scenarios

### "I just want to see if tests pass"

```bash
pip install -r test-requirements.txt
cd mcp-vectorstore
pytest tests/ -v
```

Tests run in mock mode - everything passes!

### "I want to test vectorstore with real ChromaDB"

```bash
pip install -r test-requirements.txt
pip install chromadb
cd mcp-vectorstore
pytest tests/ -v
```

### "I want full testing of everything"

```bash
pip install -r test-requirements.txt
pip install -r test-requirements-optional.txt
./run_all_tests.sh -v
```

### "I'm developing a specific server"

```bash
# Install essentials + server-specific deps
pip install -r test-requirements.txt

# For vectorstore
pip install chromadb faiss-cpu

# Then test
cd mcp-vectorstore
pytest tests/ -v --cov=src
```

## Troubleshooting

### "pytest: command not found"

```bash
pip install pytest pytest-asyncio
```

### "ModuleNotFoundError: No module named 'mcp'"

```bash
pip install mcp
```

### "Some tests are skipped"

That's normal! Tests requiring optional dependencies are automatically skipped:

```
tests/test_server.py::test_chromadb_backend SKIPPED (ChromaDB not installed)
```

Install the optional deps or ignore - other tests still validate the logic!

### "Tests fail with import errors"

Make sure you're in the server directory:

```bash
cd servers/mcp-vectorstore  # Not just servers/
pytest tests/ -v
```

## Summary

- **Minimum to test**: `pip install -r test-requirements.txt`
- **Tests work without optional deps** (mock mode)
- **Install optional deps** for full functionality
- **Use `./setup_tests.sh`** for guided setup
- **Tests auto-skip** if dependencies missing

**Bottom line**: Install essentials, run tests, they work! Add optional deps as needed for your development.
