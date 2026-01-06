"""MCP Generator Server - Response generation for RAG pipelines."""

__version__ = "0.1.0"

from .server import GeneratorManager, app, manager

__all__ = ["GeneratorManager", "app", "manager"]
