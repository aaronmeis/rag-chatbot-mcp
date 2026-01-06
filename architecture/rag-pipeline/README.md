# RAG Pipeline Architecture

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## Overview

This document describes the complete Retrieval-Augmented Generation (RAG) pipeline implemented across our MCP servers.

## Pipeline Stages

### Stage 1: Data Ingestion (mcp-datasources)

**Purpose**: Load documents from various sources

**Supported Sources**:
- Local files (PDF, TXT, MD, DOCX, HTML)
- URLs (web scraping with content extraction)
- APIs (REST endpoints with JSON/XML)
- Databases (PostgreSQL, MySQL, SQLite)
- Cloud storage (S3, GCS, Azure Blob)

**Tools**:
| Tool | Description |
|------|-------------|
| `load_files` | Load documents from local filesystem |
| `load_url` | Fetch and parse web content |
| `load_api` | Query REST API endpoints |
| `load_database` | Execute queries against databases |
| `list_sources` | List available data sources |
| `get_source_info` | Get metadata about a source |

### Stage 2: Document Processing (mcp-chunker)

**Purpose**: Split documents into optimal chunks for retrieval

**Chunking Strategies**:
- **Fixed Size**: Split by character/token count
- **Recursive**: Split by separators (paragraphs, sentences)
- **Semantic**: Split by topic/meaning changes
- **Document-Aware**: Respect document structure (headers, sections)

**Tools**:
| Tool | Description |
|------|-------------|
| `chunk_text` | Split text using specified strategy |
| `chunk_document` | Process entire document with metadata |
| `set_chunk_size` | Configure chunk size parameters |
| `set_overlap` | Configure chunk overlap |
| `preview_chunks` | Preview chunking without saving |

**Best Practices**:
- Chunk size: 256-512 tokens for most use cases
- Overlap: 10-20% of chunk size
- Preserve metadata (source, page, section)

### Stage 3: Embedding Generation (mcp-embeddings)

**Purpose**: Convert text chunks into vector representations

**Supported Models**:
| Model | Dimensions | Provider | Cost |
|-------|------------|----------|------|
| text-embedding-3-small | 1536 | OpenAI | $0.00002/1K tokens |
| text-embedding-3-large | 3072 | OpenAI | $0.00013/1K tokens |
| all-MiniLM-L6-v2 | 384 | Local | Free |
| all-mpnet-base-v2 | 768 | Local | Free |
| e5-large-v2 | 1024 | Local | Free |

**Tools**:
| Tool | Description |
|------|-------------|
| `embed_text` | Generate embedding for single text |
| `embed_batch` | Generate embeddings for multiple texts |
| `set_model` | Configure embedding model |
| `get_model_info` | Get current model details |

### Stage 4: Vector Storage (mcp-vectorstore)

**Purpose**: Store and index embeddings for efficient retrieval

**Supported Backends**:
- **ChromaDB**: Default, easy setup, good for development
- **FAISS**: High performance, Facebook's library
- **Pinecone**: Managed cloud service
- **Weaviate**: Open-source with GraphQL

**Tools**:
| Tool | Description |
|------|-------------|
| `create_collection` | Create new vector collection |
| `add_documents` | Add embeddings with metadata |
| `search_similar` | Find similar vectors |
| `delete_documents` | Remove documents from index |
| `list_collections` | List available collections |
| `get_collection_stats` | Get collection statistics |

### Stage 5: Retrieval (mcp-retriever)

**Purpose**: Find relevant documents for a query

**Retrieval Methods**:
- **Dense**: Semantic similarity using embeddings
- **Sparse**: Keyword matching (BM25, TF-IDF)
- **Hybrid**: Combination of dense + sparse

**Tools**:
| Tool | Description |
|------|-------------|
| `retrieve` | Basic retrieval with top-k results |
| `retrieve_with_filters` | Retrieval with metadata filters |
| `hybrid_search` | Combined dense + sparse search |
| `multi_query_retrieve` | Retrieve using query expansion |
| `set_retrieval_params` | Configure retrieval parameters |

### Stage 6: Reranking (mcp-reranker)

**Purpose**: Improve ranking of retrieved documents

**Reranking Methods**:
- **Cross-Encoder**: Deep scoring of query-document pairs
- **LLM-based**: Use LLM to score relevance
- **Reciprocal Rank Fusion**: Combine multiple rankings
- **Diversity**: Ensure result diversity

**Tools**:
| Tool | Description |
|------|-------------|
| `rerank` | Rerank results using cross-encoder |
| `llm_rerank` | Rerank using LLM scoring |
| `fuse_rankings` | Combine multiple result sets |
| `diversify` | Apply diversity filtering |

### Stage 7: Response Generation (mcp-generator)

**Purpose**: Generate final response using retrieved context

**Generation Modes**:
- **Standard RAG**: Context + Query → Response
- **Summarization**: Summarize retrieved documents
- **Extraction**: Extract specific information
- **Comparison**: Compare information across documents

**Tools**:
| Tool | Description |
|------|-------------|
| `generate_response` | Generate answer from context |
| `summarize_context` | Summarize retrieved documents |
| `extract_info` | Extract structured information |
| `generate_with_citations` | Generate with source citations |
| `set_prompt_template` | Configure prompt template |

## Advanced Techniques

### Query Transformation
- **HyDE**: Hypothetical Document Embeddings
- **Multi-Query**: Generate multiple query variants
- **Step-Back**: Generate more abstract queries

### Context Compression
- **Extractive**: Select relevant sentences
- **Abstractive**: Summarize context
- **Token Limiting**: Fit within context window

### Evaluation Metrics
- **Retrieval**: MRR, NDCG, Recall@K
- **Generation**: BLEU, ROUGE, BERTScore
- **End-to-End**: Answer accuracy, faithfulness

## Example Pipeline

```python
# Complete RAG pipeline example
from rag_chatbot_mcp import MCPClient

client = MCPClient()

# 1. Load documents
docs = client.call("datasources", "load_files", path="/docs")

# 2. Chunk documents
chunks = client.call("chunker", "chunk_document", 
                     documents=docs, 
                     strategy="recursive",
                     chunk_size=512)

# 3. Generate embeddings
embeddings = client.call("embeddings", "embed_batch",
                         texts=[c["text"] for c in chunks])

# 4. Store in vector database
client.call("vectorstore", "add_documents",
            collection="my_docs",
            documents=chunks,
            embeddings=embeddings)

# 5. Retrieve relevant documents
query = "What is the return policy?"
results = client.call("retriever", "retrieve",
                      query=query,
                      collection="my_docs",
                      top_k=10)

# 6. Rerank results
reranked = client.call("reranker", "rerank",
                       query=query,
                       documents=results,
                       top_k=5)

# 7. Generate response
response = client.call("generator", "generate_response",
                       query=query,
                       context=reranked)

print(response)
```

## Configuration

See individual server READMEs for detailed configuration options:
- [mcp-datasources](../../servers/mcp-datasources/README.md)
- [mcp-chunker](../../servers/mcp-chunker/README.md)
- [mcp-embeddings](../../servers/mcp-embeddings/README.md)
- [mcp-vectorstore](../../servers/mcp-vectorstore/README.md)
- [mcp-retriever](../../servers/mcp-retriever/README.md)
- [mcp-reranker](../../servers/mcp-reranker/README.md)
- [mcp-generator](../../servers/mcp-generator/README.md)
