# Quick Start Guide

> **⚠️ Under Construction**  
> This project is currently under active development. Features, APIs, and documentation may change.

Get up and running with the RAG Chatbot MCP Platform UI components in minutes!

## Prerequisites Check

1. **ChromaDB Running (Docker)**
   ```bash
   # Start ChromaDB in Docker
   docker-compose up -d chromadb
   
   # Check status
   docker-compose ps chromadb
   
   # View logs if needed
   docker-compose logs chromadb
   ```

2. **Ollama Running**
   ```bash
   # Check if Ollama is running
   ollama list
   
   # If not running, start it
   ollama serve
   
   # Pull a small model (in another terminal)
   ollama pull llama3.2:1b
   # OR
   ollama pull tinyllama
   ```

2. **Python Environment**
   ```bash
   # Check Python version (need 3.10+)
   python --version
   
   # Install UI dependencies
   pip install -r ui/requirements.txt
   
   # Install core dependencies (if not already installed)
   pip install -r requirements.txt
   ```

## Option 1: Streamlit App (Recommended for Beginners)

### Start the App

```bash
# From project root
cd ui/streamlit-app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Using the App

1. **Load Documents** (Document Loading tab)
   - Click "📥 Load Sample Documents"
   - Wait for success message

2. **Index Documents**
   - Click "🔨 Index Documents"
   - Wait for indexing to complete (may take a minute)

3. **Query** (Query & Chat tab)
   - Type your question in the chat input
   - Press Enter
   - View the response and sources

### Example Queries

- "What is RAG?"
- "How does RAG work?"
- "What are the benefits of RAG?"
- "What vector databases are supported?"

## Option 2: Jupyter Notebook (Recommended for Learning)

### Start Jupyter

```bash
# 1. Ensure ChromaDB is running
docker-compose up -d chromadb

# 2. Start Jupyter from project root
jupyter notebook

# 3. Navigate to ui/jupyter-notebook/rag_pipeline_exercise.ipynb
```

### Run the Notebook

1. **Check Prerequisites** (First cell)
   - Verifies ChromaDB connection
   - Checks Ollama availability
   - Shows connection status

2. **Run All Cells** (Cell → Run All)
   - Or run cells sequentially (Shift+Enter)

3. **Watch the Pipeline**
   - See each step execute
   - Understand the data flow
   - View intermediate results
   - ChromaDB connection status shown in first cell

4. **Experiment**
   - Modify queries in the query cells
   - Change configuration values
   - Try different models

## Troubleshooting

### "Ollama not available"
- Ensure Ollama is running: `ollama serve`
- Check model is pulled: `ollama list`
- Pull model: `ollama pull llama3.2:1b`

### "Module not found" errors
- Ensure you're in the project root
- Check Python path includes project root
- Reinstall dependencies: `pip install -r requirements.txt`

### "ChromaDB errors"
- Delete `./chroma_db` directory
- Restart the app/notebook
- Re-index documents

### "Embedding model download slow"
- First run downloads the model (~80MB)
- Ensure internet connection
- Wait for download to complete

## Next Steps

- Load your own documents
- Experiment with chunk sizes
- Try different embedding models
- Test various Ollama models
- Explore advanced features

## Getting Help

- Check `ui/README.md` for detailed documentation
- Review `architecture/README.md` for system design
- See `servers/README.md` for API details

