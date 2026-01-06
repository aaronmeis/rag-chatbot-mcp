#!/bin/bash
# Install Dependencies for RAG Chatbot MCP Platform
# Run this script to install all required dependencies

set -e

echo "=========================================="
echo "RAG Chatbot MCP - Dependency Installation"
echo "=========================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

REQUIRED_VERSION="3.10"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "ERROR: Python $REQUIRED_VERSION or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo ""
echo "Installing core dependencies..."
pip install mcp>=1.0.0

# Install vector store dependencies
echo ""
echo "Installing vector store dependencies..."
pip install chromadb>=0.4.0
pip install faiss-cpu>=1.7.0

# Install embedding dependencies
echo ""
echo "Installing embedding dependencies..."
pip install openai>=1.0.0
pip install sentence-transformers>=2.2.0

# Install document processing dependencies
echo ""
echo "Installing document processing dependencies..."
pip install pypdf>=3.0.0
pip install python-docx>=0.8.11
pip install beautifulsoup4>=4.12.0
pip install markdown>=3.4.0

# Install retrieval dependencies
echo ""
echo "Installing retrieval dependencies..."
pip install rank-bm25>=0.2.2

# Install reranking dependencies
echo ""
echo "Installing reranking dependencies..."
pip install torch>=2.0.0
pip install transformers>=4.30.0

# Install testing dependencies
echo ""
echo "Installing testing dependencies..."
pip install pytest>=7.0.0
pip install pytest-asyncio>=0.21.0
pip install pytest-cov>=4.0.0

# Install development dependencies
echo ""
echo "Installing development dependencies..."
pip install black>=23.0.0
pip install isort>=5.12.0
pip install mypy>=1.0.0

# Create requirements.txt
echo ""
echo "Generating requirements.txt..."
pip freeze > requirements.txt

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To verify installation, run:"
echo "  ./tests/manual_testing/Solution-Testing/verify_servers.sh"
echo ""
