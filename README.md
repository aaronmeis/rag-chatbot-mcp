# RAG Chatbot MCP Platform

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-2025--06--18-green.svg)](https://modelcontextprotocol.io/)
[![Claude Desktop](https://img.shields.io/badge/Claude-Desktop-orange.svg)](https://claude.ai/download)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

**AI-Orchestrated Retrieval-Augmented Generation Platform using Model Context Protocol**

Build intelligent, context-aware chatbots that leverage your own data through natural language interactions. This platform provides 7 specialized MCP servers with 35+ tools for complete RAG pipeline orchestration.


![Overview](./unnamed (2).png)


---

## 🚀 Quick Start

### Option 1: Streamlit Web App (Recommended for Beginners)

```bash
# 1. Clone repository
git clone https://github.com/your-org/rag-chatbot-mcp.git
cd rag-chatbot-mcp

# 2. Install dependencies
pip install -r requirements.txt
pip install -r ui/requirements.txt

# 3. Start ChromaDB in Docker (optional but recommended)
docker-compose up -d chromadb
# Or use: .\scripts\start_chromadb.ps1 (Windows) or ./scripts/start_chromadb.sh (Linux/Mac)

# 4. Start Ollama (in a separate terminal)
ollama serve
ollama pull llama3.2:1b  # or tinyllama

# 5. Run Streamlit app
cd ui/streamlit-app
streamlit run app.py
```

The app will open at `http://localhost:8501`. See [UI README](ui/README.md) for detailed instructions.

**Note:** ChromaDB will automatically connect to Docker if available, or use local/mock mode otherwise.

### Option 2: Jupyter Notebook (Recommended for Learning)

```bash
# 1. Clone repository
git clone https://github.com/your-org/rag-chatbot-mcp.git
cd rag-chatbot-mcp

# 2. Install dependencies
pip install -r requirements.txt
pip install -r ui/requirements.txt

# 3. Start ChromaDB in Docker (optional but recommended)
docker-compose up -d chromadb
# Or use: .\scripts\start_chromadb.ps1 (Windows) or ./scripts/start_chromadb.sh (Linux/Mac)

# 4. Start Ollama (in a separate terminal)
ollama serve
ollama pull llama3.2:1b

# 5. Start Jupyter
jupyter notebook

# 6. Open ui/jupyter-notebook/rag_pipeline_exercise.ipynb
```

**Note:** ChromaDB will automatically connect to Docker if available, or use local/mock mode otherwise.

### Option 3: Claude Desktop Integration

```bash
# 1. Clone repository
git clone https://github.com/your-org/rag-chatbot-mcp.git
cd rag-chatbot-mcp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Claude Desktop (7 MCP servers)
# macOS:
cp desktop-configs/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux:
cp desktop-configs/claude_desktop_config.json \
   ~/.config/Claude/claude_desktop_config.json

# Windows:
# Copy desktop-configs/claude_desktop_config.json to:
# %APPDATA%\Claude\claude_desktop_config.json

# 4. Restart Claude Desktop
# 5. Verify servers are connected in Claude Desktop settings
```

**Prerequisites:** 
- **Python 3.11 or 3.12** (recommended) - Python 3.14+ has ChromaDB compatibility issues
- **Docker Desktop** (recommended for ChromaDB) - [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Ollama** (for UI) - [Install Ollama](https://ollama.ai)
- Claude Desktop (optional, for MCP integration)
- 16GB RAM, 20GB disk

**Quick Setup:**
```bash
# 1. Start ChromaDB in Docker (recommended)
docker-compose up -d chromadb

# 2. Start Ollama
ollama serve
ollama pull llama3.2:1b
```

**Note:** If using Python 3.14+, ChromaDB will use mock mode (works for testing). For production, use Python 3.11 or 3.12. See [Troubleshooting](docker/TROUBLESHOOTING.md) for details.

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  🌐 Streamlit Chat UI    │   📓 Jupyter Notebook   │   💬 Claude Desktop    │
│     (Web Interface)      │   (Data Science)        │      (Local STDIO)     │
└────────────┬─────────────┴──────────┬──────────────┴──────────┬─────────────┘
             │                        │                         │
             ▼                        ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI ORCHESTRATION LAYER                                │
│                    🤖 Claude API (MCP Client Support)                        │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│ DATA INGESTION│          │   RETRIEVAL   │          │   GENERATION  │
├───────────────┤          ├───────────────┤          ├───────────────┤
│ mcp-chunker   │──────────│ mcp-retriever │──────────│ mcp-generator │
│ mcp-embeddings│          │ mcp-reranker  │          │               │
│ mcp-datasources│         │ mcp-vectorstore│         │               │
└───────────────┘          └───────────────┘          └───────────────┘
        │                            │                            │
        ▼                            ▼                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│   📄 Documents    │   🔢 Vector Store   │   📊 Indexes   │   💾 Cache      │
│   (PDF, TXT, MD)  │   (ChromaDB/FAISS)  │   (BM25/Hybrid)│   (Redis/Local) │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ MCP Servers Overview

| Server | Tools | Status | Description |
|--------|-------|--------|-------------|
| **mcp-vectorstore** | 6 | ✅ Production | Vector database operations, similarity search, index management |
| **mcp-retriever** | 5 | ✅ Production | Document retrieval, hybrid search, metadata filtering |
| **mcp-embeddings** | 4 | ✅ Production | Embedding generation (OpenAI, local models, batch processing) |
| **mcp-chunker** | 5 | ✅ Production | Document chunking, text splitting, preprocessing |
| **mcp-reranker** | 4 | ✅ Production | Result reranking, cross-encoder scoring, diversity filtering |
| **mcp-generator** | 5 | ✅ Production | Response generation, context assembly, prompt templates |
| **mcp-datasources** | 6 | ✅ Production | External connectors (files, URLs, APIs, databases) |

**Total: 7 servers, 35+ tools**

---

## 📁 Project Structure

```
rag-chatbot-mcp/
├── README.md                           # This file
├── LICENSE                             # Apache 2.0
├── ACKNOWLEDGMENTS.md                  # Credits and references
├── .gitignore                          # Git ignore patterns
│
├── architecture/                       # System design documentation
│   ├── README.md                       # Architecture overview
│   ├── diagrams/                       # Mermaid diagrams, architecture images
│   └── rag-pipeline/                   # RAG pipeline detailed design
│
├── data/                               # Data files and samples
│   ├── sample-data/                    # Example documents for testing
│   ├── embeddings/                     # Pre-computed embeddings
│   └── indexes/                        # Vector indexes
│
├── desktop-configs/                    # Claude Desktop configurations
│   └── claude_desktop_config.json      # MCP server configuration
│
├── docs/                               # Documentation
│   ├── operations/                     # Operations guides
│   ├── deployment/                     # Deployment instructions
│   └── user-guides/                    # User documentation
│
├── infrastructure/                     # Deployment infrastructure
│   ├── gcp/                            # Google Cloud Platform setup
│   └── local/                          # Local development setup
│
├── scripts/                            # Utility scripts
│   ├── setup.sh                        # Initial setup
│   └── deploy.sh                       # Deployment automation
│
├── servers/                            # MCP Server implementations
│   ├── mcp-vectorstore/                # Vector database server
│   ├── mcp-retriever/                  # Retrieval server
│   ├── mcp-embeddings/                 # Embeddings server
│   ├── mcp-chunker/                    # Document chunking server
│   ├── mcp-reranker/                   # Reranking server
│   ├── mcp-generator/                  # Response generation server
│   └── mcp-datasources/                # Data source connectors
│
├── shared/                             # Shared utilities
│   ├── utils/                          # Common utilities
│   ├── models/                         # Data models
│   └── config/                         # Configuration management
│
├── tests/                              # Test suites
│   ├── integration/                    # Integration tests
│   └── manual_testing/                 # Manual testing guides
│
└── ui/                                 # User interfaces
    ├── streamlit-app/                  # Web chat interface (app.py)
    ├── jupyter-notebook/              # Notebook interface (rag_pipeline_exercise.ipynb)
    ├── README.md                       # UI components documentation
    ├── QUICKSTART.md                   # Quick start guide
    └── requirements.txt                # UI-specific dependencies
```

---

## 🎯 Who is this For?

### 🔬 AI/ML Engineers
*You want to build production RAG systems with modular, testable components*

**What you can do:**
- Build custom RAG pipelines with interchangeable components
- Experiment with different embedding models and retrieval strategies
- Implement advanced techniques (HyDE, step-back prompting, multi-query)
- Scale from prototype to production with the same architecture
- Use interactive UIs (Streamlit/Jupyter) for rapid prototyping

**Quick Start:**
1. [Streamlit App](ui/README.md#streamlit-app) - Interactive web interface for testing
2. [Jupyter Notebook](ui/README.md#jupyter-notebook) - Step-by-step pipeline exploration
3. [RAG Pipeline Guide](tests/manual_testing/RAG-Pipeline/README.md) - Detailed pipeline docs
4. [Sample Data](data/sample-data/README.md) - Example documents
5. [Server APIs](servers/README.md) - Complete API reference

---

### 💻 MCP Developers
*You want to learn MCP patterns or extend the platform*

**What you can learn:**
- MCP server architecture and best practices
- Testing patterns (unit, integration, functional)
- Tool design for LLM orchestration
- Production deployment strategies

**Development Resources:**
- [Architecture Deep Dive](architecture/README.md)
- [Server Implementation Guide](docs/development/SERVER_GUIDE.md)
- [Testing Guide](tests/manual_testing/Solution-Testing/MANUAL_TESTING_GUIDE.md)

---

### 🛠️ Software Engineers
*You want to deploy, integrate, or scale this system*

**Deployment Scenarios:**

| Environment | Setup | Resources | Use Case |
|-------------|-------|-----------|----------|
| **Local Development** | MacOS/Linux + Claude Desktop | 16GB RAM, 20GB disk | Development, testing |
| **Cloud Research** | GCP Cloud Run | Custom (scalable) | Production, multi-user |
| **Enterprise** | Kubernetes + GPU | 32GB+ RAM | High-throughput RAG |

**Infrastructure Resources:**
- [GCP Deployment Guide](infrastructure/gcp/README.md)
- [Local Setup](infrastructure/local/README.md)
- [Claude Desktop Config](desktop-configs/README.md)

---

### 🎓 Students & Educators
*You want to learn RAG concepts hands-on*

**Why this is perfect for teaching:**
- ✅ **Modular design** - Learn each RAG component separately
- ✅ **Sample data included** - Ready to run examples
- ✅ **Well-documented** - Step-by-step guides with expected outputs
- ✅ **Low cost** - Run locally with free/cheap models
- ✅ **Interactive UIs** - Streamlit app and Jupyter notebook for hands-on learning

**Educational Topics:**
- Vector embeddings and similarity search
- Document chunking strategies
- Retrieval and reranking techniques
- Prompt engineering for RAG
- Evaluation and metrics

**Quick Start for Students:**
1. [Streamlit App](ui/README.md#streamlit-app) - Visual, interactive interface
2. [Jupyter Notebook](ui/README.md#jupyter-notebook) - Step-by-step exploration
3. [Sample Data](data/sample-data/) - Ready-to-use documents

---

## 💰 Cost Analysis

| Mode | Time | Cost | Use Case |
|------|------|------|----------|
| **Demo (Local UI)** | 5-10 min | **$0** | Testing with Streamlit/Jupyter + Ollama |
| **Demo (Cloud)** | 5-10 min | ~$0.10 | Testing with OpenAI embeddings + Claude API |
| **Development** | 30-60 min | ~$1-2 | Building features |
| **Production** | Continuous | ~$10-50/day | Deployed chatbot |

*Local UI mode (Streamlit/Jupyter + Ollama + sentence-transformers) has $0 operational cost. Cloud mode uses OpenAI embeddings + Claude API.*

---

## 🏃 Example Usage

### Using the Streamlit Web App

1. **Load Documents**: Click "📥 Load Sample Documents" in the Document Loading tab
2. **Index Documents**: Click "🔨 Index Documents" to chunk, embed, and store documents
3. **Query**: Switch to Query & Chat tab and ask questions like:
   - "What is RAG?"
   - "How does RAG work?"
   - "What are the benefits of RAG?"

### Using the Jupyter Notebook

Run cells sequentially to see each step of the RAG pipeline:
- Load sample documents
- Chunk documents with different strategies
- Generate embeddings
- Store in vector database
- Query and retrieve relevant chunks
- Generate responses with Ollama

### Natural Language RAG Operations (Claude Desktop)

```
User: "Load all the PDF documents from my /docs folder"
Claude: [Uses mcp-datasources to load files, mcp-chunker to process them]

User: "Create embeddings and index them"
Claude: [Uses mcp-embeddings to generate vectors, mcp-vectorstore to index]

User: "What does the documentation say about authentication?"
Claude: [Uses mcp-retriever for search, mcp-reranker for relevance, mcp-generator for response]

User: "Show me the most similar documents to this query"
Claude: [Uses mcp-vectorstore for similarity search, returns ranked results]
```

---

## 🔧 Configuration

### Claude Desktop Configuration

The platform includes **7 MCP servers** configured for Claude Desktop. Copy the configuration file:

```bash
cp desktop-configs/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Configured Servers:**
1. `rag-vectorstore` - Vector database operations
2. `rag-embeddings` - Embedding generation
3. `rag-retriever` - Document retrieval
4. `rag-chunker` - Document chunking
5. `rag-reranker` - Result reranking
6. `rag-generator` - Response generation
7. `rag-datasources` - Data source connectors

**Example Configuration:**
```json
{
  "mcpServers": {
    "rag-vectorstore": {
      "command": "python",
      "args": ["-m", "servers.mcp-vectorstore.src.server"],
      "cwd": "${workspaceFolder}"
    },
    "rag-embeddings": {
      "command": "python",
      "args": ["-m", "servers.mcp-embeddings.src.server"],
      "cwd": "${workspaceFolder}"
    }
    // ... 5 additional servers (see desktop-configs/claude_desktop_config.json)
  }
}
```

See `desktop-configs/claude_desktop_config.json` for the complete configuration with all 7 servers and environment variables.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [UI Components Guide](ui/README.md) | **NEW!** Streamlit app and Jupyter notebook usage |
| [UI Quick Start](ui/QUICKSTART.md) | **NEW!** Quick start guide for UI components |
| [ChromaDB Docker Setup](docker/README.md) | **NEW!** Running ChromaDB in Docker |
| [Architecture Overview](architecture/README.md) | System design and data flow |
| [RAG Pipeline Guide](architecture/rag-pipeline/README.md) | Detailed pipeline documentation |
| [Server Reference](servers/README.md) | Complete API documentation |
| [Deployment Guide](docs/deployment/README.md) | Production deployment |
| [User Guide](docs/user-guides/README.md) | End-user documentation |
| [Testing Guide](tests/manual_testing/Solution-Testing/MANUAL_TESTING_GUIDE.md) | Testing procedures |

---

## 🤝 Contributing

Contributions welcome! Priority areas include:
- New embedding model integrations
- Additional vector store backends
- Advanced retrieval strategies
- UI improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

This project is inspired by the [precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) project structure. See [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md) for full credits.
