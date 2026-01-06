# RAG Chatbot MCP Platform - UI Components

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

This directory contains user interfaces for exercising the RAG Chatbot MCP Platform.
![Overview](./unnamed(2).png)
## Components

### 1. Streamlit App (`streamlit-app/`)

A web-based chat interface for interacting with the RAG system.

**Features:**
- Load and index documents
- Interactive chat interface
- Real-time query processing
- Source document display
- Configuration options

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
cd streamlit-app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 2. Jupyter Notebook (`jupyter-notebook/`)

An interactive notebook for exploring the RAG pipeline step-by-step.

**Features:**
- Step-by-step RAG pipeline execution
- Document loading and chunking
- Embedding generation
- Vector store operations
- Query and retrieval examples
- Helper functions for experimentation

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook

# Open rag_pipeline_exercise.ipynb
```

## Prerequisites

1. **ChromaDB (Recommended: Docker)**
   - **Option A - Docker (Recommended)**: `docker-compose up -d chromadb`
   - **Option B - Local**: Install ChromaDB locally (may have issues on Windows)
   - **Option C - Mock Mode**: Works without ChromaDB but with limited functionality
   - See [ChromaDB Docker Setup](../docker/README.md) for details

2. **Ollama Running Locally**
   - Install Ollama from https://ollama.ai
   - Start Ollama: `ollama serve`
   - Pull a small model: `ollama pull llama3.2:1b` or `ollama pull tinyllama`

3. **Python Dependencies**
   - Install from `requirements.txt` in the project root
   - Install UI-specific dependencies from `ui/requirements.txt`

4. **Sample Data**
   - Sample documents are in `data/sample-data/`
   - The apps will automatically load these

## Quick Start

### Streamlit App

1. **Start ChromaDB** (recommended): `docker-compose up -d chromadb`
2. **Start Ollama**: `ollama serve` (in a separate terminal)
3. **Pull a model**: `ollama pull llama3.2:1b`
4. **Run the app**: `streamlit run ui/streamlit-app/app.py`
5. Click "Load Sample Documents" in the Document Loading tab
6. Click "Index Documents"
7. Switch to "Query & Chat" tab and start asking questions!

### Jupyter Notebook

1. **Start ChromaDB** (recommended): `docker-compose up -d chromadb`
2. **Start Ollama**: `ollama serve` (in a separate terminal)
3. **Pull a model**: `ollama pull llama3.2:1b`
4. **Start Jupyter**: `jupyter notebook`
5. **Open**: `ui/jupyter-notebook/rag_pipeline_exercise.ipynb`
6. **Run all cells** sequentially (or run cells one by one)
7. Modify queries and experiment!

## Configuration

### Streamlit App
- **Ollama Model**: Select from dropdown (llama3.2:1b, tinyllama, etc.)
- **Collection Name**: Name for the vector collection
- **Embedding Model**: Local sentence-transformers model
- **Chunk Size**: Size of document chunks (256-1024)
- **Chunk Overlap**: Overlap between chunks (0-200)
- **Top K**: Number of retrieved documents (1-10)

### Jupyter Notebook
Edit the configuration cell:
```python
COLLECTION_NAME = "rag_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2:1b"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
TOP_K = 3
```

## Troubleshooting

### Ollama Connection Errors
- Ensure Ollama is running: `ollama serve`
- Check model is available: `ollama list`
- Pull the model if needed: `ollama pull llama3.2:1b`

### Import Errors
- Ensure you're running from the project root
- Check that all dependencies are installed
- Verify Python path includes project root

### ChromaDB Errors
- **Docker not running**: Start ChromaDB with `docker-compose up -d chromadb`
- **Port conflict**: Change port in `docker-compose.yml` if 8000 is in use
- **Connection issues**: Check ChromaDB logs with `docker-compose logs chromadb`
- **Python 3.14 compatibility**: ChromaDB has issues with Python 3.14+ (pydantic v1). Use Python 3.11/3.12 or mock mode
- **Local ChromaDB**: Delete `./chroma_db` directory if corrupted
- **Mock mode**: If ChromaDB unavailable, the app will use mock mode (limited functionality but works for testing)
- See [ChromaDB Troubleshooting](../docker/TROUBLESHOOTING.md) for detailed solutions

### Embedding Model Errors
- First run will download the model (may take time)
- Ensure internet connection for model download
- Check disk space for model storage

## Architecture

Both interfaces use the same underlying MCP server managers:
- `DataSourcesManager`: Load documents
- `ChunkerManager`: Split documents into chunks
- `EmbeddingManager`: Generate embeddings
- `VectorStoreManager`: Store and search vectors
- `RetrieverManager`: Retrieve relevant documents
- `ollama`: Generate responses (replaces mock generator)

The pipeline flow:
1. Load documents → 2. Chunk → 3. Embed → 4. Store → 5. Retrieve → 6. Generate

## Next Steps

- Experiment with different chunk sizes and strategies
- Try different embedding models
- Test various Ollama models
- Load your own documents
- Explore advanced retrieval techniques


