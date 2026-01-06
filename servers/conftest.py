"""
Shared configuration for all MCP server tests.

This file is automatically discovered by pytest when running tests from the servers/ directory.
It provides common configuration and utilities for all server test suites.
"""

import sys
import os
import warnings

# Suppress warnings for cleaner test output
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

# Add servers directory to path
servers_dir = os.path.dirname(os.path.abspath(__file__))
if servers_dir not in sys.path:
    sys.path.insert(0, servers_dir)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "requires_chromadb: marks tests that require ChromaDB"
    )
    config.addinivalue_line(
        "markers", "requires_openai: marks tests that require OpenAI API"
    )
    config.addinivalue_line(
        "markers", "requires_internet: marks tests that require internet connection"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically skip tests that require unavailable dependencies."""
    # Check for optional dependencies
    try:
        import chromadb
        has_chromadb = True
    except ImportError:
        has_chromadb = False

    try:
        import openai
        has_openai = True
    except ImportError:
        has_openai = False

    skip_chromadb = None
    skip_openai = None

    if not has_chromadb:
        skip_chromadb = "ChromaDB not installed (pip install chromadb)"
    if not has_openai:
        skip_openai = "OpenAI not installed (pip install openai)"

    # Apply skips
    for item in items:
        if "requires_chromadb" in item.keywords and skip_chromadb:
            item.add_marker(pytest.mark.skip(reason=skip_chromadb))
        if "requires_openai" in item.keywords and skip_openai:
            item.add_marker(pytest.mark.skip(reason=skip_openai))


# Import pytest for markers
import pytest
