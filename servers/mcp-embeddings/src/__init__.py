"""MCP Embeddings Server - Embedding generation using various models."""

__version__ = "0.1.0"

from .server import EmbeddingManager, app, manager

__all__ = ["EmbeddingManager", "app", "manager"]
