# Architecture Overview

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

## System Design

The RAG Chatbot MCP Platform follows a modular, microservices-inspired architecture where each component of the RAG pipeline is implemented as an independent MCP server.

## Design Principles

### 1. Separation of Concerns
Each MCP server handles a specific responsibility:
- **Data Ingestion**: Loading, parsing, and preprocessing documents
- **Indexing**: Creating and managing vector representations
- **Retrieval**: Finding relevant information
- **Generation**: Producing responses

### 2. Composability
Servers can be combined in different ways to create custom pipelines:
- Simple Q&A: retriever → generator
- Advanced RAG: chunker → embeddings → vectorstore → retriever → reranker → generator
- Hybrid Search: retriever (BM25) + vectorstore (semantic) → reranker

### 3. Scalability
- Each server can be deployed independently
- Horizontal scaling per component based on load
- Stateless design enables easy replication

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INGESTION PHASE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │   Documents  │────▶│  mcp-chunker │────▶│   Chunks     │
    │  (PDF, TXT)  │     │              │     │              │
    └──────────────┘     └──────────────┘     └──────┬───────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │mcp-embeddings│
                                              │              │
                                              └──────┬───────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │mcp-vectorstore│
                                              │   (Index)    │
                                              └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              RETRIEVAL PHASE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │    Query     │────▶│mcp-retriever │────▶│   Results    │
    │              │     │              │     │              │
    └──────────────┘     └──────────────┘     └──────┬───────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │ mcp-reranker │
                                              │              │
                                              └──────┬───────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │   Ranked     │
                                              │   Results    │
                                              └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                             GENERATION PHASE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │   Context    │────▶│mcp-generator │────▶│   Response   │
    │  + Query     │     │              │     │              │
    └──────────────┘     └──────────────┘     └──────────────┘
```

## Server Communication

All servers communicate through the MCP protocol:
- **STDIO**: Local development with Claude Desktop
- **SSE**: Cloud deployment with HTTP transport
- **WebSocket**: Real-time streaming (optional)

## State Management

| Component | State Location | Persistence |
|-----------|---------------|-------------|
| Vector Store | ChromaDB/FAISS | Disk |
| Document Cache | Redis/Memory | Configurable |
| Session History | Memory | Session |
| Configuration | YAML/ENV | Disk |

## Security Considerations

- API keys stored in environment variables
- Document access controlled per-user
- Audit logging for all operations
- Rate limiting on public endpoints

## See Also

- [RAG Pipeline Details](rag-pipeline/README.md)
- [Server Implementations](../servers/README.md)
- [Deployment Guide](../docs/deployment/README.md)
