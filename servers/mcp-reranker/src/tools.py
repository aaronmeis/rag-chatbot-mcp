"""
Tool implementations for MCP Reranker Server.

This module contains the core reranking logic.
"""

# Note: The RerankerManager class is currently in server.py.
# For this implementation, we're using the existing implementation
# in server.py to avoid duplication.

# Import the manager from server for consistency
from .server import RerankerManager

__all__ = ["RerankerManager"]
