"""MCP Reranker Server - Result reranking for improved retrieval quality."""

__version__ = "0.1.0"

from .server import RerankerManager, app, manager

__all__ = ["RerankerManager", "app", "manager"]
