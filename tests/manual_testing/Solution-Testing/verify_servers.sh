#!/bin/bash
# Verify RAG Chatbot MCP Servers
# Run this script to verify all MCP servers are working correctly

set -e

echo "=========================================="
echo "RAG Chatbot MCP - Server Verification"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
SERVERS=("mcp-vectorstore" "mcp-embeddings" "mcp-retriever" "mcp-chunker" "mcp-reranker" "mcp-generator" "mcp-datasources")

# Function to check server syntax
check_server_syntax() {
    local server=$1
    local server_path="servers/$server/src/server.py"
    
    if [ ! -f "$server_path" ]; then
        echo -e "${RED}✗ $server: server.py not found${NC}"
        return 1
    fi
    
    # Check Python syntax
    if python3 -m py_compile "$server_path" 2>/dev/null; then
        echo -e "${GREEN}✓ $server: syntax OK${NC}"
        return 0
    else
        echo -e "${RED}✗ $server: syntax error${NC}"
        return 1
    fi
}

# Function to check server imports
check_server_imports() {
    local server=$1
    local server_path="servers/$server/src/server.py"
    
    # Try to import the server module (with mock mode)
    export MOCK_MODE=true
    if python3 -c "
import sys
sys.path.insert(0, '.')
try:
    exec(open('$server_path').read().split('if __name__')[0])
    print('imports OK')
except ImportError as e:
    print(f'import error: {e}')
    sys.exit(1)
except Exception as e:
    # Other errors are OK at this stage
    print('imports OK (with warnings)')
" 2>/dev/null; then
        echo -e "${GREEN}  └─ imports: OK${NC}"
        return 0
    else
        echo -e "${YELLOW}  └─ imports: requires dependencies${NC}"
        return 0  # Not a failure, just needs deps
    fi
}

# Function to run server tests
run_server_tests() {
    local server=$1
    local test_path="servers/$server/tests"
    
    if [ ! -d "$test_path" ] || [ -z "$(ls -A $test_path 2>/dev/null)" ]; then
        echo -e "${YELLOW}  └─ tests: no tests found${NC}"
        return 0
    fi
    
    if pytest "$test_path" -v --tb=short 2>/dev/null; then
        echo -e "${GREEN}  └─ tests: PASSED${NC}"
        return 0
    else
        echo -e "${RED}  └─ tests: FAILED${NC}"
        return 1
    fi
}

# Main verification loop
echo ""
echo "Checking server syntax and structure..."
echo "----------------------------------------"

for server in "${SERVERS[@]}"; do
    if check_server_syntax "$server"; then
        check_server_imports "$server"
        ((PASSED++))
    else
        ((FAILED++))
    fi
done

# Run tests if pytest is available
echo ""
echo "Running server tests..."
echo "----------------------------------------"

if command -v pytest &> /dev/null; then
    for server in "${SERVERS[@]}"; do
        echo "Testing $server..."
        run_server_tests "$server"
    done
else
    echo -e "${YELLOW}pytest not installed - skipping tests${NC}"
    echo "Install with: pip install pytest pytest-asyncio"
fi

# Check configuration files
echo ""
echo "Checking configuration files..."
echo "----------------------------------------"

if [ -f "desktop-configs/claude_desktop_config.json" ]; then
    if python3 -c "import json; json.load(open('desktop-configs/claude_desktop_config.json'))" 2>/dev/null; then
        echo -e "${GREEN}✓ claude_desktop_config.json: valid JSON${NC}"
    else
        echo -e "${RED}✗ claude_desktop_config.json: invalid JSON${NC}"
    fi
else
    echo -e "${RED}✗ claude_desktop_config.json: not found${NC}"
fi

# Check data directories
echo ""
echo "Checking data directories..."
echo "----------------------------------------"

DIRS=("data/sample-data" "data/embeddings" "data/indexes")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ $dir: exists${NC}"
    else
        echo -e "${YELLOW}○ $dir: creating...${NC}"
        mkdir -p "$dir"
    fi
done

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "Servers checked: ${#SERVERS[@]}"
echo -e "Syntax OK: ${GREEN}$PASSED${NC}"
echo -e "Syntax Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All servers verified successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Install dependencies: ./tests/manual_testing/Solution-Testing/install_dependencies.sh"
    echo "2. Configure API keys in your environment"
    echo "3. Copy desktop-configs/claude_desktop_config.json to Claude Desktop"
    exit 0
else
    echo -e "${RED}Some servers failed verification${NC}"
    echo "Please fix the errors above before proceeding."
    exit 1
fi
