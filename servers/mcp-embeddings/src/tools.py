"""
Tool implementations for MCP Embeddings Server.

This module contains the core embedding generation logic.
"""

# Note: The EmbeddingManager class is currently in server.py.
# For this implementation, we're using the existing implementation
# in server.py to avoid duplication.

# Import the manager from server for consistency
from .server import EmbeddingManager

__all__ = ["EmbeddingManager"]
