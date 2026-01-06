"""MCP Chunker Server - Document chunking and preprocessing."""

__version__ = "0.1.0"

from .server import ChunkerManager, app, manager

__all__ = ["ChunkerManager", "app", "manager"]
