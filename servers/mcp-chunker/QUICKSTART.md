# MCP Chunker - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
cd servers/mcp-chunker
pip install -e .
```

## Dependencies

Required:
- `mcp>=0.1.0` - MCP SDK

No additional dependencies required for basic chunking!

## Running the Server

```bash
python -m servers.mcp_chunker.src.server
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "rag-chunker": {
      "command": "python",
      "args": ["-m", "servers.mcp_chunker.src.server"]
    }
  }
}
```

## Available Tools

1. **chunk_text** - Split text using specified strategy
2. **chunk_document** - Process document with metadata
3. **set_chunk_size** - Configure default chunk size
4. **set_overlap** - Configure chunk overlap
5. **preview_chunks** - Preview without saving

## Chunking Strategies

### Fixed Size
- Splits text into fixed character lengths
- Supports overlap for context preservation

### Recursive
- Splits by natural boundaries (paragraphs, sentences, words)
- Best for general-purpose use
- **Recommended default**

### Sentence
- Groups sentences to target chunk size
- Preserves sentence boundaries
- Good for Q&A and semantic tasks

### Paragraph
- Splits by paragraph breaks
- Preserves document structure
- Best for structured documents

## Example Usage

### Basic Text Chunking

```json
{
  "text": "Your long document text here...",
  "strategy": "recursive",
  "chunk_size": 512,
  "overlap": 50
}
```

### Document with Metadata

```json
{
  "document": {
    "text": "Document content...",
    "metadata": {
      "source": "document.pdf",
      "author": "John Doe",
      "date": "2024-01-01"
    }
  },
  "strategy": "sentence"
}
```

### Preview Chunks

```json
{
  "text": "Test document...",
  "strategy": "recursive"
}
```

Returns chunk preview with statistics!

## Configuration

### Set Default Chunk Size

```json
{
  "size": 1024
}
```

### Set Default Overlap

```json
{
  "overlap": 100
}
```

## Best Practices

### Choosing Chunk Size
- **Small (256-512)**: Better precision, more chunks
- **Medium (512-1024)**: Balanced approach (recommended)
- **Large (1024-2048)**: More context, fewer chunks

### Choosing Overlap
- **No overlap (0)**: Faster, no duplication
- **Small overlap (50-100)**: Preserves some context
- **Large overlap (100-200)**: Maximum context preservation

### Strategy Selection
- **Recursive**: Default, works well for most content
- **Sentence**: Q&A, semantic search, summarization
- **Paragraph**: Structured docs, maintaining sections
- **Fixed**: When exact sizes needed

## Testing

```bash
pytest tests/test_server.py -v
pytest tests/test_tools.py -v

# Test specific strategy
pytest tests/test_tools.py::test_recursive_chunking -v
```

## Integration Example

```python
# 1. Chunk documents
chunker.chunk_text(text="...", strategy="recursive")

# 2. Generate embeddings
embeddings.embed_batch(texts=[chunk["text"] for chunk in chunks])

# 3. Store in vectorstore
vectorstore.add_documents(documents=chunks, embeddings=embeddings)
```

## Troubleshooting

**Chunks too small**: Increase chunk_size

**Losing context**: Increase overlap

**Too many chunks**: Increase chunk_size or try paragraph strategy

**Sentences split awkwardly**: Use sentence or recursive strategy

## Next Steps

- Review [README.md](README.md) for advanced features
- Experiment with different strategies
- Test with your actual documents
- Integrate with embeddings and vectorstore servers
