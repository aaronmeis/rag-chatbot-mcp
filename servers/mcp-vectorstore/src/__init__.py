"""MCP VectorStore Server - Vector database operations for RAG pipelines."""

__version__ = "0.1.0"

from .server import VectorStoreManager, app, manager

__all__ = ["VectorStoreManager", "app", "manager"]
