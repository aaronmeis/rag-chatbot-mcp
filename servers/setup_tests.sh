#!/bin/bash

# Test Environment Setup Script
# This script sets up the testing environment for all MCP servers

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}MCP Servers - Test Environment Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
echo -e "Python version: ${GREEN}$python_version${NC}"
echo ""

# Ask about installation type
echo -e "${YELLOW}Choose installation type:${NC}"
echo "1) Essential only (core testing, works in mock mode)"
echo "2) Full installation (all optional dependencies)"
echo "3) Custom (choose specific servers)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo -e "${BLUE}Installing essential test requirements...${NC}"
        pip install -r test-requirements.txt
        echo -e "${GREEN}✓ Essential requirements installed${NC}"
        ;;
    2)
        echo -e "${BLUE}Installing all requirements...${NC}"
        pip install -r test-requirements.txt
        pip install -r test-requirements-optional.txt
        echo -e "${GREEN}✓ All requirements installed${NC}"
        ;;
    3)
        echo -e "${BLUE}Installing essential requirements first...${NC}"
        pip install -r test-requirements.txt
        echo ""

        echo -e "${YELLOW}Select servers to install dependencies for:${NC}"
        echo "1) mcp-vectorstore (chromadb, faiss)"
        echo "2) mcp-embeddings (openai, sentence-transformers)"
        echo "3) mcp-datasources (parsers for PDF, DOCX, etc)"
        echo "4) All of the above"
        echo ""
        read -p "Enter choices (comma-separated, e.g., 1,2): " servers

        IFS=',' read -ra SELECTED <<< "$servers"
        for server in "${SELECTED[@]}"; do
            case $server in
                1|*vectorstore*)
                    echo -e "${BLUE}Installing vectorstore dependencies...${NC}"
                    pip install chromadb faiss-cpu
                    ;;
                2|*embeddings*)
                    echo -e "${BLUE}Installing embeddings dependencies...${NC}"
                    pip install openai sentence-transformers torch
                    ;;
                3|*datasources*)
                    echo -e "${BLUE}Installing datasources dependencies...${NC}"
                    pip install beautifulsoup4 PyPDF2 python-docx pandas
                    ;;
                4|*all*)
                    echo -e "${BLUE}Installing all optional dependencies...${NC}"
                    pip install -r test-requirements-optional.txt
                    ;;
            esac
        done
        echo -e "${GREEN}✓ Custom requirements installed${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Verifying Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Verify pytest is installed
if python -m pytest --version > /dev/null 2>&1; then
    pytest_version=$(python -m pytest --version)
    echo -e "${GREEN}✓ pytest installed:${NC} $pytest_version"
else
    echo -e "${RED}✗ pytest not found${NC}"
    exit 1
fi

# Check for MCP SDK
if python -c "import mcp" 2>/dev/null; then
    echo -e "${GREEN}✓ MCP SDK installed${NC}"
else
    echo -e "${YELLOW}⚠ MCP SDK not found (required for running servers)${NC}"
    echo -e "  Install with: pip install mcp"
fi

# Check optional dependencies
echo ""
echo -e "${YELLOW}Optional Dependencies Status:${NC}"

# ChromaDB
if python -c "import chromadb" 2>/dev/null; then
    echo -e "${GREEN}✓ ChromaDB${NC} (vectorstore)"
else
    echo -e "${YELLOW}○ ChromaDB${NC} (vectorstore will use mock mode)"
fi

# OpenAI
if python -c "import openai" 2>/dev/null; then
    echo -e "${GREEN}✓ OpenAI${NC} (embeddings)"
else
    echo -e "${YELLOW}○ OpenAI${NC} (embeddings will use mock mode)"
fi

# BeautifulSoup
if python -c "import bs4" 2>/dev/null; then
    echo -e "${GREEN}✓ BeautifulSoup${NC} (HTML parsing)"
else
    echo -e "${YELLOW}○ BeautifulSoup${NC} (limited HTML support)"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Quick Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Run a quick test if user wants
read -p "Run a quick test to verify setup? [y/N]: " run_test

if [[ $run_test =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Running quick test...${NC}"

    # Try to run vectorstore tests
    if [ -d "mcp-vectorstore/tests" ]; then
        cd mcp-vectorstore
        if python -m pytest tests/test_server.py::TestVectorStoreManager::test_create_collection -v; then
            echo -e "${GREEN}✓ Quick test passed!${NC}"
        else
            echo -e "${RED}✗ Quick test failed${NC}"
            echo -e "${YELLOW}This is normal if MCP SDK is not installed${NC}"
        fi
        cd ..
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Run tests: ${BLUE}./run_all_tests.sh -v${NC}"
echo -e "  2. Or test single server: ${BLUE}cd mcp-vectorstore && pytest tests/ -v${NC}"
echo -e "  3. Read the guide: ${BLUE}cat TEST_GUIDE.md${NC}"
echo ""
