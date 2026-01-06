"""MCP DataSources Server - Load documents from various sources."""

__version__ = "0.1.0"

from .server import DataSourcesManager, app, manager

__all__ = ["DataSourcesManager", "app", "manager"]
