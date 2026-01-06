"""MCP Retriever Server - Document retrieval with multiple search strategies."""

__version__ = "0.1.0"

from .server import RetrieverManager, app, manager

__all__ = ["RetrieverManager", "app", "manager"]
