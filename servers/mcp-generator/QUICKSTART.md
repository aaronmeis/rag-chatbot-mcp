# MCP Generator - Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Installation

```bash
cd servers/mcp-generator
pip install -e .

# For LLM integration
pip install -e ".[llm]"
```

## Dependencies

Required:
- `mcp>=0.1.0` - MCP SDK

Optional:
- `openai>=1.0.0` - For OpenAI models
- `anthropic` - For Claude models

## Running the Server

```bash
python -m servers.mcp_generator.src.server
```

### With LLM Provider

```bash
export OPENAI_API_KEY=your-key
# or
export ANTHROPIC_API_KEY=your-key

python -m servers.mcp_generator.src.server
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "rag-generator": {
      "command": "python",
      "args": ["-m", "servers.mcp_generator.src.server"],
      "env": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Available Tools

1. **generate_response** - Generate answer from context
2. **summarize_context** - Summarize documents
3. **extract_info** - Extract structured information
4. **generate_with_citations** - Generate with citations
5. **set_prompt_template** - Configure prompt templates

## Prompt Templates

### Default
General-purpose Q&A template

### Concise
Brief, to-the-point answers

### Detailed
Comprehensive answers with explanations

### Citation
Answers with source citations [1], [2], etc.

## Example Usage

### Basic Generation

```json
{
  "query": "What is machine learning?",
  "context": [
    {
      "text": "Machine learning is a subset of AI...",
      "metadata": {"source": "intro.pdf"}
    },
    {
      "text": "ML algorithms learn from data...",
      "metadata": {"source": "guide.md"}
    }
  ],
  "template": "default"
}
```

### Generate with Citations

```json
{
  "query": "How do neural networks work?",
  "context": [
    {"text": "Neural networks consist of layers...", "metadata": {"source": "nn.pdf"}},
    {"text": "Each layer transforms the input...", "metadata": {"source": "dl.md"}}
  ]
}
```

Response will include [1], [2] references to sources.

### Summarize Context

```json
{
  "documents": [
    {"text": "Document 1 content..."},
    {"text": "Document 2 content..."},
    {"text": "Document 3 content..."}
  ],
  "max_length": 500
}
```

### Extract Structured Info

```json
{
  "documents": [...],
  "schema": {
    "type": "object",
    "properties": {
      "main_topic": {"type": "string"},
      "key_points": {"type": "array"},
      "confidence": {"type": "number"}
    }
  }
}
```

### Custom Template

```json
{
  "name": "my_template",
  "template": "Answer the question using context.\n\nContext:\n{context}\n\nQuestion: {query}\n\nYour answer:"
}
```

## Template Variables

Templates support these variables:
- `{context}` - Formatted context documents
- `{query}` - User query
- `{num_docs}` - Number of context documents

## Context Formatting

Documents are automatically formatted as:

```
[1] source.pdf:
Document text here...

[2] guide.md:
Another document...
```

## Complete RAG Pipeline

```
1. Load documents (datasources)
2. Chunk documents (chunker)
3. Generate embeddings (embeddings)
4. Store vectors (vectorstore)
5. Retrieve relevant docs (retriever)
6. Rerank results (reranker)
7. Generate answer (generator) ← You are here!
```

## Testing

```bash
pytest tests/test_server.py -v
pytest tests/test_tools.py -v

# Test specific template
pytest tests/test_tools.py::test_citation_template -v
```

## Best Practices

### Context Quality
- Provide 3-10 relevant documents
- Remove irrelevant documents
- Rerank before generating

### Template Selection
- **default**: General questions
- **concise**: Quick facts, definitions
- **detailed**: Complex topics, explanations
- **citation**: When sources matter

### Prompt Engineering
- Keep templates focused
- Include clear instructions
- Test with various queries

## Integration Example

```python
# After retrieval and reranking
top_docs = reranker.rerank(query, documents, top_k=5)

# Generate answer
response = generator.generate_response(
    query=query,
    context=top_docs,
    template="citation"
)
```

## Troubleshooting

**Generic responses**: Provide more specific context documents

**Missing information**: Increase number of context documents

**Hallucinations**: Use citation template, verify against sources

**Too long/short**: Adjust template or try different template type

## Next Steps

- Review [README.md](README.md) for advanced features
- Create custom templates for your use case
- Test with real queries and documents
- Integrate with full RAG pipeline
- Experiment with different LLM providers
