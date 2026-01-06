# mcp-datasources

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Data source connectors MCP server for loading documents.

## Overview

The `mcp-datasources` server provides tools for loading documents from various sources including files, URLs, APIs, and databases.

## Features

- File loading (PDF, TXT, MD, DOCX, HTML)
- Web scraping
- API integration
- Database connectors

## Tools

### load_files

Load documents from filesystem.

**Parameters:**
- `path` (string, required): File or directory path
- `pattern` (string, optional): File pattern (e.g., "*.pdf")
- `recursive` (bool, optional): Search subdirectories

### load_url

Fetch and parse web content.

**Parameters:**
- `url` (string, required): URL to fetch
- `extract_text` (bool, optional): Extract text only

### load_api

Query REST API endpoint.

**Parameters:**
- `url` (string, required): API endpoint
- `method` (string, optional): HTTP method
- `headers` (object, optional): Request headers
- `body` (object, optional): Request body

### load_database

Execute database query.

**Parameters:**
- `connection_string` (string, required): Database connection
- `query` (string, required): SQL query

### list_sources

List available data sources.

### get_source_info

Get metadata about a source.

**Parameters:**
- `source_id` (string, required): Source identifier

## Supported File Types

| Extension | Parser |
|-----------|--------|
| `.pdf` | PyPDF2/pdfplumber |
| `.txt` | Plain text |
| `.md` | Markdown |
| `.docx` | python-docx |
| `.html` | BeautifulSoup |
| `.json` | JSON parser |
| `.csv` | CSV parser |

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-datasources
source venv-datasources/bin/activate  # On Windows: venv-datasources\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: Full datasources functionality
pip install beautifulsoup4 PyPDF2 python-docx pandas sqlalchemy
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional dependencies for full functionality
pip install beautifulsoup4 PyPDF2 python-docx pandas
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

# Specific test file
pytest tests/test_server.py -v
pytest tests/test_tools.py -v

# Specific test
pytest tests/test_server.py::TestFileLoading::test_load_single_text_file -v
```

### What Gets Tested

- ✅ File loading (txt, md, json, csv)
- ✅ Directory traversal (recursive/non-recursive)
- ✅ URL fetching (mock)
- ✅ API querying (mock)
- ✅ Database loading (mock)
- ✅ Metadata extraction
- ✅ Error handling

**Note:** Tests work in mock mode without optional dependencies. Install `beautifulsoup4`, `PyPDF2`, etc. for real parsing.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide
