#!/bin/bash
# RAG Chatbot MCP - Quick Setup Script

set -e

echo "🚀 Setting up RAG Chatbot MCP Platform..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/indexes
mkdir -p data/embeddings

# Verify installation
echo "✅ Verifying installation..."
python -c "import mcp; print(f'MCP version: {mcp.__version__}')" 2>/dev/null || echo "MCP installed"
python -c "import chromadb; print('ChromaDB: OK')"
python -c "import sentence_transformers; print('Sentence Transformers: OK')"

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'"
echo "  2. Run a server: python -m servers.mcp-vectorstore.src.server"
echo "  3. Run tests: pytest servers/mcp-vectorstore/tests/ -v"
echo ""
