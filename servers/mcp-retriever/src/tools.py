"""
Tool implementations for MCP Retriever Server.

This module contains the core retrieval logic, extracted from server.py
for better modularity and testing.
"""

# Note: The RetrieverManager class is currently in server.py.
# For this implementation, we're using the existing implementation
# in server.py to avoid duplication.

# Import the manager from server for consistency
from .server import RetrieverManager

__all__ = ["RetrieverManager"]
