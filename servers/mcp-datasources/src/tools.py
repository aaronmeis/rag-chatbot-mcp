"""
Tool implementations for MCP DataSources Server.

This module contains the core data loading logic.
"""

# Note: The DataSourcesManager class is currently in server.py.
# For this implementation, we're using the existing implementation
# in server.py to avoid duplication.

# Import the manager from server for consistency
from .server import DataSourcesManager

__all__ = ["DataSourcesManager"]
