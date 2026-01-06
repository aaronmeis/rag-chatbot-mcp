# Environment Management Guide

This guide explains when to use separate virtual environments vs a shared environment for MCP server development and testing.

## TL;DR

- **Individual Server Development**: Use separate virtual environments (`venv-{servername}`)
- **End-to-End Testing**: Use a shared environment in the `servers/` directory
- **Quick Testing**: Use mock mode with minimal dependencies

## Philosophy

The MCP server architecture supports two testing workflows:

1. **Isolated Development**: Work on one server independently without interference
2. **Integration Testing**: Test the full RAG pipeline with all servers working together

## Separate Environments (Individual Servers)

### When to Use

- Developing or debugging a single MCP server
- Testing server-specific functionality
- Running unit tests for one server
- Avoiding dependency conflicts between servers

### How to Set Up

Each server can have its own isolated virtual environment:

```bash
# For mcp-vectorstore
cd servers/mcp-vectorstore
python -m venv venv-vectorstore
source venv-vectorstore/bin/activate  # Windows: venv-vectorstore\Scripts\activate
pip install -e .
pip install -r ../test-requirements.txt

# For mcp-embeddings
cd servers/mcp-embeddings
python -m venv venv-embeddings
source venv-embeddings/bin/activate  # Windows: venv-embeddings\Scripts\activate
pip install -e .
pip install -r ../test-requirements.txt

# Repeat for other servers...
```

### Benefits

✅ No dependency conflicts between servers
✅ Minimal installation per server
✅ Fast setup and teardown
✅ Easy to test different dependency versions
✅ Clean separation of concerns

### Example Workflow

```bash
# Work on vectorstore
cd servers/mcp-vectorstore
source venv-vectorstore/bin/activate
pytest tests/ -v
# Make changes...
pytest tests/ -v --cov=src

# Switch to embeddings
deactivate
cd ../mcp-embeddings
source venv-embeddings/bin/activate
pytest tests/ -v
```

## Shared Environment (End-to-End Testing)

### When to Use

- Testing the complete RAG pipeline
- Running integration tests across multiple servers
- Developing features that span multiple servers
- Running the full test suite

### How to Set Up

Create a single shared environment in the `servers/` directory:

```bash
cd servers/

# Create shared environment
python -m venv venv-shared
source venv-shared/bin/activate  # Windows: venv-shared\Scripts\activate

# Install all servers
pip install -e mcp-datasources
pip install -e mcp-chunker
pip install -e mcp-embeddings
pip install -e mcp-vectorstore
pip install -e mcp-retriever
pip install -e mcp-reranker
pip install -e mcp-generator

# Install test requirements
pip install -r test-requirements.txt

# Optional: Install all optional dependencies for full functionality
pip install -r test-requirements-optional.txt
```

### Benefits

✅ Test full RAG pipeline
✅ Catch integration issues
✅ Verify server interactions
✅ Run end-to-end tests
✅ Single environment to manage

### Example Workflow

```bash
cd servers/
source venv-shared/bin/activate

# Run all tests
./run_all_tests.sh -v

# Or test specific integration scenarios
pytest mcp-vectorstore/tests/ mcp-embeddings/tests/ -v

# Run end-to-end pipeline test
python examples/full_rag_pipeline.py
```

## Quick Comparison

| Aspect | Separate Environments | Shared Environment |
|--------|----------------------|-------------------|
| **Setup Time** | Fast per server | Slower (install all) |
| **Disk Space** | More (multiple venvs) | Less (one venv) |
| **Isolation** | Perfect | None |
| **Integration Testing** | Limited | Full |
| **Dependency Conflicts** | Avoided | Possible |
| **Use Case** | Individual development | End-to-end testing |

## Recommended Workflow

### For Development

1. **Start with separate environments** for the server(s) you're working on
2. Run unit tests in isolated environment
3. Make your changes
4. Verify tests pass in isolation

### For Integration

1. **Switch to shared environment** before merging/releasing
2. Run integration tests across servers
3. Test the full RAG pipeline
4. Verify no dependency conflicts

### For CI/CD

Consider both approaches:

```yaml
# Example GitHub Actions workflow
jobs:
  unit-tests:
    # Use separate environments for unit tests
    strategy:
      matrix:
        server: [vectorstore, embeddings, retriever, ...]
    steps:
      - name: Test ${{ matrix.server }}
        run: |
          cd servers/mcp-${{ matrix.server }}
          python -m venv venv
          source venv/bin/activate
          pip install -e .
          pip install -r ../test-requirements.txt
          pytest tests/ -v

  integration-tests:
    # Use shared environment for integration
    steps:
      - name: Setup shared environment
        run: |
          cd servers/
          python -m venv venv-shared
          source venv-shared/bin/activate
          pip install -e mcp-*/
          pip install -r test-requirements.txt
      - name: Run integration tests
        run: ./servers/run_all_tests.sh -v
```

## Environment Variables

Some servers require environment variables for full functionality:

```bash
# For embeddings (OpenAI)
export OPENAI_API_KEY=your_key_here

# For vectorstore (custom backend)
export VECTORSTORE_BACKEND=chromadb
export VECTORSTORE_PATH=./data

# For embeddings (model selection)
export EMBEDDING_MODEL=text-embedding-3-small
```

**Note:** Tests work in mock mode without these variables. Set them for real API testing.

## Troubleshooting

### "ImportError: No module named X"

**Separate Environment:**
```bash
# Ensure you're in the right environment
which python
# Should show: servers/mcp-{server}/venv-{server}/bin/python

# Reinstall dependencies
pip install -e .
pip install -r ../test-requirements.txt
```

**Shared Environment:**
```bash
# Ensure you're in shared environment
which python
# Should show: servers/venv-shared/bin/python

# Reinstall all servers
cd servers/
pip install -e mcp-*/
```

### "Tests fail in shared environment but pass individually"

This suggests a dependency conflict or state sharing issue:

1. Check for different dependency versions
2. Look for shared state between servers
3. Run tests with `-v` to see details
4. Try `pytest --lf` to run only failed tests

### "Too many virtual environments to manage"

Use a helper script:

```bash
# servers/activate.sh
#!/bin/bash

if [ "$1" == "shared" ]; then
    source venv-shared/bin/activate
else
    cd "mcp-$1"
    source "venv-$1/bin/activate"
fi
```

Usage:
```bash
source servers/activate.sh vectorstore  # Activate venv-vectorstore
source servers/activate.sh shared       # Activate venv-shared
```

## Best Practices

1. **Name environments consistently**: `venv-{servername}` or `venv-shared`
2. **Add to .gitignore**: Don't commit virtual environments
3. **Document dependencies**: Keep pyproject.toml and requirements files updated
4. **Test in both modes**: Unit tests isolated, integration tests shared
5. **Clean up regularly**: Remove old environments with `rm -rf venv-*`

## Mock Mode vs Real Dependencies

All tests support mock mode with minimal dependencies:

```bash
# Essential only (works for all servers)
pip install -r test-requirements.txt
# Installs: pytest, mcp, numpy

# Tests will:
# ✅ Run successfully
# ✅ Use mock implementations
# ✅ Test business logic
# ❌ Not use real APIs/databases
```

For full functionality, install optional dependencies per server:

```bash
# Vectorstore: Real vector databases
pip install chromadb faiss-cpu

# Embeddings: Real embedding models
pip install openai sentence-transformers torch

# Datasources: Real file parsers
pip install beautifulsoup4 PyPDF2 python-docx pandas
```

## Quick Reference Commands

### Separate Environments

```bash
# Create and activate for specific server
cd servers/mcp-{servername}
python -m venv venv-{servername}
source venv-{servername}/bin/activate
pip install -e .
pip install -r ../test-requirements.txt
pytest tests/ -v
```

### Shared Environment

```bash
# Create and activate shared environment
cd servers/
python -m venv venv-shared
source venv-shared/bin/activate
pip install -e mcp-*/
pip install -r test-requirements.txt
./run_all_tests.sh -v
```

### Switch Between Environments

```bash
# Deactivate current environment
deactivate

# Activate different environment
source venv-{servername}/bin/activate  # or venv-shared/bin/activate
```

## See Also

- [QUICK_TEST_SETUP.md](QUICK_TEST_SETUP.md) - Fast setup guide
- [TESTING_README.md](TESTING_README.md) - Testing infrastructure overview
- [TEST_GUIDE.md](TEST_GUIDE.md) - Comprehensive testing guide
- Individual server READMEs for server-specific installation instructions
