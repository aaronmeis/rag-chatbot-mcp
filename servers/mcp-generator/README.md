# mcp-generator

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Response generation MCP server for RAG pipelines.

## Overview

The `mcp-generator` server provides tools for generating responses using retrieved context.

## Features

- Context-aware generation
- Multiple prompt templates
- Citation support
- Summarization mode

## Installation

### For Development (Isolated Environment)

```bash
# Create isolated environment for this server
python -m venv venv-generator
source venv-generator/bin/activate  # On Windows: venv-generator\Scripts\activate

# Install this server
pip install -e .

# Install test dependencies
pip install -r ../test-requirements.txt

# Optional: LLM providers
pip install openai anthropic
```

### For Testing Only

```bash
# Essential only (tests work in mock mode)
pip install -r ../test-requirements.txt

# Optional: LLM API access
pip install openai anthropic
```

## Tools

### generate_response

Generate answer from context.

**Parameters:**
- `query` (string, required): User query
- `context` (array, required): Retrieved documents
- `template` (string, optional): Prompt template name

### summarize_context

Summarize retrieved documents.

**Parameters:**
- `documents` (array, required): Documents to summarize
- `max_length` (int, optional): Maximum summary length

### extract_info

Extract structured information.

**Parameters:**
- `documents` (array, required): Source documents
- `schema` (object, required): Extraction schema

### generate_with_citations

Generate response with source citations.

**Parameters:**
- `query` (string, required): User query
- `context` (array, required): Retrieved documents

### set_prompt_template

Configure custom prompt template.

**Parameters:**
- `name` (string, required): Template name
- `template` (string, required): Template content

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

# Test specific features
pytest tests/ -v -k "generation"
pytest tests/ -v -k "citation"
pytest tests/ -v -k "summarize"
```

### What Gets Tested

- ✅ Context-aware response generation
- ✅ Multiple prompt templates
- ✅ Citation generation and tracking
- ✅ Context summarization
- ✅ Structured information extraction
- ✅ Template management
- ✅ Error handling
- ✅ Mock mode (without LLM APIs)

**Note:** Tests work in mock mode without OpenAI/Anthropic API keys. Install them for real generation.

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [../TEST_GUIDE.md](../TEST_GUIDE.md) - Comprehensive testing guide
- [../QUICK_TEST_SETUP.md](../QUICK_TEST_SETUP.md) - Fast setup guide
