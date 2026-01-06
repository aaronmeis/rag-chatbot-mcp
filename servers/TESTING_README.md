# Testing Infrastructure Overview

## What We Built

A comprehensive, flexible testing infrastructure for all 7 MCP servers that balances **ease of setup** with **optional full functionality**.

## Key Philosophy

✅ **Tests run independently** - Each server can be tested without the others
✅ **Mock mode by default** - Essential deps only, tests work out of the box
✅ **Optional enhancements** - Install real implementations as needed
✅ **Graceful degradation** - Tests auto-skip if dependencies unavailable

## Files Created

### Shared Test Infrastructure

```
servers/
├── test-requirements.txt           # Essential deps (REQUIRED)
├── test-requirements-optional.txt  # Optional deps (for full functionality)
├── setup_tests.sh                  # Interactive setup script
├── run_all_tests.sh               # Run all server tests
├── conftest.py                    # Shared pytest configuration
├── QUICK_TEST_SETUP.md            # Quick start guide
├── TEST_GUIDE.md                  # Comprehensive testing guide
└── TESTING_SUMMARY.md             # Implementation details
```

### Per-Server Test Files (× 7 servers)

```
mcp-{server}/
├── tests/
│   ├── conftest.py       # Fixtures with sample data
│   ├── test_server.py    # Integration tests
│   └── test_tools.py     # Unit tests
├── src/
│   ├── tools.py         # Business logic
│   └── utils.py         # Helper functions
├── pyproject.toml       # Package config
└── QUICKSTART.md        # Server-specific guide
```

## Quick Start

### For Developers Who Want to Run Tests Now

```bash
# 1. Install essentials (< 1 minute)
pip install -r servers/test-requirements.txt

# 2. Test any server (works immediately!)
cd servers/mcp-vectorstore
pytest tests/ -v
```

**That's it!** Tests run in mock mode without optional dependencies.

### For Developers Who Want Full Functionality

```bash
# Interactive setup
cd servers
./setup_tests.sh

# Or manual full install
pip install -r test-requirements.txt
pip install -r test-requirements-optional.txt
```

## Testing Approaches

### Approach 1: Minimal Setup (Fastest)

**Install:** Essential deps only (`~5 packages`)
**Time:** 30 seconds
**What works:** All tests pass in mock mode
**Best for:** CI/CD, quick validation, new developers

```bash
pip install -r servers/test-requirements.txt
cd servers/mcp-vectorstore && pytest tests/ -v
```

### Approach 2: Full Setup (Complete)

**Install:** All dependencies (`~20 packages`)
**Time:** 2-3 minutes
**What works:** Real implementations, full functionality
**Best for:** Development, integration testing

```bash
./servers/setup_tests.sh  # Choose option 2
```

### Approach 3: Custom Setup (Targeted)

**Install:** Essential + specific servers
**Time:** 1 minute
**What works:** Real implementation for chosen servers
**Best for:** Working on specific servers

```bash
./servers/setup_tests.sh  # Choose option 3
# Select: 1 (vectorstore) + 2 (embeddings)
```

## Dependency Tiers

### Tier 1: Essential (Required)

**5 packages** - Needed for any testing

```
pytest, pytest-asyncio, pytest-cov, mcp, numpy
```

Install: `pip install -r test-requirements.txt`

### Tier 2: Server-Specific (Optional)

Choose what you need:

| Server | Optional Deps | Enables |
|--------|--------------|---------|
| vectorstore | chromadb, faiss-cpu | Real vector DBs |
| embeddings | openai, sentence-transformers | Real embeddings |
| datasources | beautifulsoup4, PyPDF2, pandas | Real parsers |
| Others | None needed | Already work fully |

### Tier 3: Development Tools (Nice to have)

```
black, ruff, mypy, pytest-html, pytest-xdist
```

For code quality and parallel testing.

## Mock Mode vs Real Mode

### What is Mock Mode?

When optional dependencies aren't installed, servers use **mock implementations**:

- **Vectorstore**: In-memory dictionaries instead of ChromaDB
- **Embeddings**: Random numpy arrays instead of OpenAI API
- **Datasources**: Simple text extraction instead of PDF parsing

### Why Mock Mode?

✅ **Fast setup** - No large dependencies
✅ **CI/CD friendly** - Minimal requirements
✅ **Tests still validate** - Business logic works
✅ **New developer friendly** - Works immediately

### When to Use Real Mode?

- Integration testing with actual services
- Performance testing
- Debugging implementation-specific issues
- Production-like testing

## Running Tests

### Single Server, Single Test

```bash
cd servers/mcp-vectorstore
pytest tests/test_server.py::TestVectorStoreManager::test_create_collection -v
```

### Single Server, All Tests

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
open htmlcov/index.html
```

### Skip Slow Tests

```bash
pytest tests/ -v -m "not slow"
```

### Only Tests That Work Without Optional Deps

```bash
pytest tests/ -v -m "not requires_chromadb and not requires_openai"
```

## Test Data & Fixtures

Every server has comprehensive fixtures in `conftest.py`:

### Example: mcp-vectorstore

```python
@pytest.fixture
def sample_documents():
    """5 AI/ML themed documents"""
    return ["Machine learning is...", ...]

@pytest.fixture
def sample_embeddings():
    """1536-dimension vectors"""
    return [[0.1]*1536, [0.2]*1536, ...]

@pytest.fixture
def populated_collection():
    """Ready-to-use collection with data"""
    # Returns manager + collection + data
```

### Example: mcp-datasources

```python
@pytest.fixture
def temp_text_file():
    """Creates & cleanup temporary .txt file"""

@pytest.fixture
def temp_directory():
    """Directory with multiple test files"""
```

All fixtures are **self-contained** and **cleanup automatically**.

## Continuous Integration

### Minimal CI (Fastest)

```yaml
- name: Test
  run: |
    pip install -r servers/test-requirements.txt
    cd servers && ./run_all_tests.sh
```

Runs in ~2 minutes, tests all servers in mock mode.

### Full CI (Complete)

```yaml
- name: Test with full deps
  run: |
    pip install -r servers/test-requirements.txt
    pip install -r servers/test-requirements-optional.txt
    cd servers && ./run_all_tests.sh -c  # with coverage
```

Runs in ~5 minutes, tests with real implementations.

## Documentation

- **[QUICK_TEST_SETUP.md](QUICK_TEST_SETUP.md)** - Start here! 2-minute setup
- **[TEST_GUIDE.md](TEST_GUIDE.md)** - Comprehensive guide with all details
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Implementation details
- **Per-server QUICKSTART.md** - Server-specific setup

## Common Commands Reference

```bash
# Setup
./setup_tests.sh                    # Interactive setup
pip install -r test-requirements.txt # Minimal setup

# Running
pytest tests/ -v                     # Verbose output
pytest tests/ -v -s                  # With print statements
pytest tests/ --collect-only         # See what will run
pytest tests/ -k "test_name"        # Run specific test

# Coverage
pytest tests/ --cov=src              # Coverage report
pytest tests/ --cov=src --cov-report=html

# Markers
pytest tests/ -m integration         # Only integration tests
pytest tests/ -m "not slow"         # Skip slow tests

# Debugging
pytest tests/ --pdb                  # Drop to debugger on failure
pytest tests/ -v --tb=short         # Short traceback
pytest tests/ -vv                    # Very verbose

# All servers
./run_all_tests.sh                   # Run all
./run_all_tests.sh -v               # Verbose
./run_all_tests.sh -c               # With coverage
./run_all_tests.sh -f               # Fast (skip slow tests)
```

## Best Practices

### For New Developers

1. Install minimal deps: `pip install -r test-requirements.txt`
2. Run tests to verify setup: `pytest tests/ -v`
3. Start developing - tests work!
4. Install optional deps as needed for your server

### For CI/CD

1. Use minimal setup for speed
2. Cache pip dependencies
3. Run with `-m "not slow"` if needed
4. Use `--tb=short` for cleaner output

### For Production Testing

1. Install full dependencies
2. Run with coverage: `--cov=src`
3. Test with real backends
4. Use integration test markers

## Summary

**The testing infrastructure is flexible:**

- ✅ **Minimum**: Install 5 packages, tests work
- ✅ **Maximum**: Install everything, full functionality
- ✅ **Custom**: Pick what you need
- ✅ **Independent**: Each server tests alone
- ✅ **Graceful**: Auto-handles missing deps

**Quick start for anyone:**

```bash
pip install -r servers/test-requirements.txt
cd servers/mcp-vectorstore
pytest tests/ -v
```

That's it!
