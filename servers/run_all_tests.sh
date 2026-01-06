#!/bin/bash

# Script to run tests for all MCP servers
# Usage: ./run_all_tests.sh [options]
#
# Options:
#   -v, --verbose    Verbose output
#   -c, --coverage   Generate coverage reports
#   -f, --fast       Skip slow tests
#   -h, --help       Show this help message

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default options
VERBOSE=""
COVERAGE=""
MARKERS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="-v -s"
            shift
            ;;
        -c|--coverage)
            COVERAGE="--cov=src --cov-report=term-missing"
            shift
            ;;
        -f|--fast)
            MARKERS='-m "not slow"'
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose    Verbose output"
            echo "  -c, --coverage   Generate coverage reports"
            echo "  -f, --fast       Skip slow tests"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running tests for all MCP servers${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Array of servers
SERVERS=(
    "mcp-vectorstore"
    "mcp-retriever"
    "mcp-embeddings"
    "mcp-chunker"
    "mcp-reranker"
    "mcp-generator"
    "mcp-datasources"
)

# Track failures
FAILED_SERVERS=()
PASSED_SERVERS=()

# Run tests for each server
for server in "${SERVERS[@]}"; do
    echo -e "${YELLOW}Testing: ${server}${NC}"
    echo "----------------------------------------"

    if [ -d "$server/tests" ]; then
        cd "$server"

        # Run pytest
        if eval "pytest tests/ $VERBOSE $COVERAGE $MARKERS"; then
            echo -e "${GREEN}✓ ${server} tests passed${NC}"
            PASSED_SERVERS+=("$server")
        else
            echo -e "${RED}✗ ${server} tests failed${NC}"
            FAILED_SERVERS+=("$server")
        fi

        cd ..
    else
        echo -e "${RED}✗ ${server} tests directory not found${NC}"
        FAILED_SERVERS+=("$server")
    fi

    echo ""
done

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${GREEN}Passed (${#PASSED_SERVERS[@]}):${NC}"
for server in "${PASSED_SERVERS[@]}"; do
    echo -e "  ${GREEN}✓${NC} $server"
done
echo ""

if [ ${#FAILED_SERVERS[@]} -gt 0 ]; then
    echo -e "${RED}Failed (${#FAILED_SERVERS[@]}):${NC}"
    for server in "${FAILED_SERVERS[@]}"; do
        echo -e "  ${RED}✗${NC} $server"
    done
    echo ""
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
