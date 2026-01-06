# MCP DataSources - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
cd servers/mcp-datasources
pip install -e .

# For full support
pip install -e ".[all]"
```

## Dependencies

Required:
- `mcp>=0.1.0` - MCP SDK

Optional (by source type):
- `requests` - For URL and API loading
- `beautifulsoup4` - For HTML parsing
- `PyPDF2` or `pdfplumber` - For PDF files
- `python-docx` - For Word documents
- `pandas` - For CSV files
- `sqlalchemy` - For database connections

## Running the Server

```bash
python -m servers.mcp_datasources.src.server
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "rag-datasources": {
      "command": "python",
      "args": ["-m", "servers.mcp_datasources.src.server"]
    }
  }
}
```

## Available Tools

1. **load_files** - Load from filesystem
2. **load_url** - Fetch web content
3. **load_api** - Query REST APIs
4. **load_database** - Execute database queries
5. **list_sources** - List registered sources
6. **get_source_info** - Get source metadata

## Supported File Types

- `.txt` - Plain text
- `.md` - Markdown
- `.pdf` - PDF documents
- `.docx` - Word documents
- `.html`, `.htm` - HTML files
- `.json` - JSON data
- `.csv` - CSV files

## Example Usage

### Load Single File

```json
{
  "path": "/path/to/document.txt"
}
```

### Load Directory

```json
{
  "path": "/path/to/documents",
  "pattern": "*.md",
  "recursive": true
}
```

### Load from URL

```json
{
  "url": "https://example.com/article",
  "extract_text": true
}
```

### Query API

```json
{
  "url": "https://api.example.com/data",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer token"
  }
}
```

### Query Database

```json
{
  "connection_string": "postgresql://user:pass@localhost/db",
  "query": "SELECT id, content FROM documents WHERE category = 'AI'"
}
```

### List All Sources

```json
{}
```

Returns all registered data sources with metadata.

## File Loading Patterns

### All Markdown Files

```json
{
  "path": "./docs",
  "pattern": "*.md",
  "recursive": false
}
```

### All Documents Recursively

```json
{
  "path": "./content",
  "pattern": "*",
  "recursive": true
}
```

### Specific File Types

```json
{
  "path": "./research",
  "pattern": "*.{pdf,docx}",
  "recursive": true
}
```

## Database Connection Strings

### PostgreSQL
```
postgresql://username:password@localhost:5432/database
```

### MySQL
```
mysql://username:password@localhost:3306/database
```

### SQLite
```
sqlite:///path/to/database.db
```

## Complete Ingestion Pipeline

```
1. Load documents (datasources) ← You are here!
2. Chunk documents (chunker)
3. Generate embeddings (embeddings)
4. Store in vectorstore (vectorstore)
```

## Testing

```bash
pytest tests/test_server.py -v
pytest tests/test_tools.py -v

# Test specific source type
pytest tests/test_tools.py::test_load_files -v
pytest tests/test_tools.py::test_load_url -v
```

## Integration Example

```python
# 1. Load documents
result = datasources.load_files(
    path="./docs",
    pattern="*.md",
    recursive=True
)

# 2. Extract documents
documents = result["documents"]

# 3. Chunk each document
chunks = []
for doc in documents:
    chunked = chunker.chunk_document(
        document={
            "text": doc["content"],
            "metadata": doc["metadata"]
        }
    )
    chunks.extend(chunked["chunks"])

# 4. Generate embeddings
embeddings = embeddings_service.embed_batch(
    texts=[c["text"] for c in chunks]
)

# 5. Store in vectorstore
vectorstore.add_documents(
    documents=chunks,
    embeddings=embeddings["embeddings"]
)
```

## Best Practices

### File Loading
- Use specific patterns to avoid loading unwanted files
- Enable recursive for nested directories
- Check file sizes before loading large files

### URL Loading
- Set appropriate timeouts
- Handle rate limiting
- Cache responses when possible

### API Loading
- Use proper authentication
- Handle pagination for large datasets
- Implement retry logic

### Database Loading
- Use connection pooling
- Limit query results
- Index frequently queried columns

## Troubleshooting

**File not found**: Check path is absolute and file exists

**Permission denied**: Ensure read permissions on files/directories

**URL timeout**: Increase timeout or check network connectivity

**Database connection failed**: Verify connection string and credentials

**Unsupported file type**: Add parser or convert file first

## Security Notes

- **Never commit connection strings** with passwords
- **Use environment variables** for sensitive data
- **Validate file paths** to prevent directory traversal
- **Sanitize database queries** to prevent SQL injection

## Next Steps

- Review [README.md](README.md) for detailed API
- Set up your data sources
- Test with sample files
- Integrate with chunker and embeddings servers
- Build your complete ingestion pipeline
