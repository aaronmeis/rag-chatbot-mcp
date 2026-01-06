"""
MCP DataSources Server

Load documents from various sources (files, URLs, APIs, databases).
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional, List, Dict

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    Server = None
    stdio_server = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSourcesManager:
    """Manages data source operations."""
    
    SUPPORTED_EXTENSIONS = {
        ".txt": "text",
        ".md": "markdown",
        ".pdf": "pdf",
        ".docx": "docx",
        ".html": "html",
        ".htm": "html",
        ".json": "json",
        ".csv": "csv"
    }
    
    def __init__(self):
        self.sources = {}
        self.source_counter = 0
    
    def _read_text_file(self, path: str) -> str:
        """Read plain text file."""
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def _parse_file(self, path: str) -> Dict:
        """Parse file based on extension."""
        ext = Path(path).suffix.lower()
        file_type = self.SUPPORTED_EXTENSIONS.get(ext, "unknown")
        
        try:
            if file_type in ["text", "markdown"]:
                content = self._read_text_file(path)
            elif file_type == "json":
                with open(path, 'r') as f:
                    data = json.load(f)
                content = json.dumps(data, indent=2)
            elif file_type == "csv":
                content = self._read_text_file(path)
            else:
                # For PDF, DOCX, HTML - mock content
                content = f"[Content from {Path(path).name} - requires additional parser]"
            
            return {
                "status": "success",
                "path": path,
                "type": file_type,
                "content": content,
                "size": len(content),
                "metadata": {
                    "filename": Path(path).name,
                    "extension": ext,
                    "source": path
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "path": path,
                "error": str(e)
            }
    
    def load_files(self, path: str, pattern: str = "*", 
                  recursive: bool = False) -> dict:
        """Load documents from filesystem."""
        path_obj = Path(path)
        documents = []
        
        if path_obj.is_file():
            # Single file
            doc = self._parse_file(str(path_obj))
            if doc["status"] == "success":
                documents.append(doc)
        elif path_obj.is_dir():
            # Directory
            glob_method = path_obj.rglob if recursive else path_obj.glob
            for file_path in glob_method(pattern):
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        doc = self._parse_file(str(file_path))
                        if doc["status"] == "success":
                            documents.append(doc)
        else:
            return {
                "status": "error",
                "message": f"Path not found: {path}"
            }
        
        # Register source
        self.source_counter += 1
        source_id = f"files_{self.source_counter}"
        self.sources[source_id] = {
            "type": "files",
            "path": path,
            "pattern": pattern,
            "document_count": len(documents)
        }
        
        return {
            "status": "success",
            "source_id": source_id,
            "path": path,
            "pattern": pattern,
            "recursive": recursive,
            "documents": documents,
            "count": len(documents)
        }
    
    def load_url(self, url: str, extract_text: bool = True) -> dict:
        """Fetch and parse web content."""
        # Mock URL loading
        content = f"[Content from {url} - requires HTTP client]"
        
        self.source_counter += 1
        source_id = f"url_{self.source_counter}"
        self.sources[source_id] = {
            "type": "url",
            "url": url
        }
        
        return {
            "status": "success",
            "source_id": source_id,
            "url": url,
            "document": {
                "content": content,
                "metadata": {
                    "source": url,
                    "type": "webpage"
                }
            },
            "text_extracted": extract_text
        }
    
    def load_api(self, url: str, method: str = "GET",
                headers: Optional[Dict] = None,
                body: Optional[Dict] = None) -> dict:
        """Query REST API endpoint."""
        # Mock API response
        response_data = {
            "message": f"Mock response from {url}",
            "method": method
        }
        
        self.source_counter += 1
        source_id = f"api_{self.source_counter}"
        self.sources[source_id] = {
            "type": "api",
            "url": url,
            "method": method
        }
        
        return {
            "status": "success",
            "source_id": source_id,
            "url": url,
            "method": method,
            "response": response_data,
            "document": {
                "content": json.dumps(response_data),
                "metadata": {
                    "source": url,
                    "type": "api",
                    "method": method
                }
            }
        }
    
    def load_database(self, connection_string: str, query: str) -> dict:
        """Execute database query."""
        # Mock database response
        mock_results = [
            {"id": 1, "text": "Sample database record 1"},
            {"id": 2, "text": "Sample database record 2"}
        ]
        
        self.source_counter += 1
        source_id = f"db_{self.source_counter}"
        self.sources[source_id] = {
            "type": "database",
            "connection": connection_string[:20] + "...",
            "query": query[:50]
        }
        
        documents = [
            {
                "content": json.dumps(row),
                "metadata": {
                    "source": "database",
                    "query": query,
                    "row_id": row.get("id")
                }
            }
            for row in mock_results
        ]
        
        return {
            "status": "success",
            "source_id": source_id,
            "query": query,
            "documents": documents,
            "count": len(documents)
        }
    
    def list_sources(self) -> dict:
        """List available data sources."""
        return {
            "status": "success",
            "sources": [
                {
                    "id": source_id,
                    **source_info
                }
                for source_id, source_info in self.sources.items()
            ],
            "count": len(self.sources)
        }
    
    def get_source_info(self, source_id: str) -> dict:
        """Get metadata about a source."""
        if source_id not in self.sources:
            return {
                "status": "error",
                "message": f"Source not found: {source_id}"
            }
        
        return {
            "status": "success",
            "source_id": source_id,
            **self.sources[source_id]
        }


# Initialize
app = Server("mcp-datasources") if Server else None
manager = DataSourcesManager()

TOOLS = [
    Tool(
        name="load_files",
        description="Load documents from filesystem",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or directory path"},
                "pattern": {"type": "string", "default": "*"},
                "recursive": {"type": "boolean", "default": False}
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="load_url",
        description="Fetch and parse web content",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "extract_text": {"type": "boolean", "default": True}
            },
            "required": ["url"]
        }
    ),
    Tool(
        name="load_api",
        description="Query REST API endpoint",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "method": {"type": "string", "default": "GET"},
                "headers": {"type": "object"},
                "body": {"type": "object"}
            },
            "required": ["url"]
        }
    ),
    Tool(
        name="load_database",
        description="Execute database query",
        inputSchema={
            "type": "object",
            "properties": {
                "connection_string": {"type": "string"},
                "query": {"type": "string"}
            },
            "required": ["connection_string", "query"]
        }
    ),
    Tool(
        name="list_sources",
        description="List all registered data sources",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="get_source_info",
        description="Get metadata about a data source",
        inputSchema={
            "type": "object",
            "properties": {
                "source_id": {"type": "string"}
            },
            "required": ["source_id"]
        }
    )
]

if app:
    @app.list_tools()
    async def list_tools():
        return TOOLS

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "load_files":
                result = manager.load_files(**arguments)
            elif name == "load_url":
                result = manager.load_url(**arguments)
            elif name == "load_api":
                result = manager.load_api(**arguments)
            elif name == "load_database":
                result = manager.load_database(**arguments)
            elif name == "list_sources":
                result = manager.list_sources()
            elif name == "get_source_info":
                result = manager.get_source_info(**arguments)
            else:
                result = {"error": f"Unknown tool: {name}"}
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            logger.error(f"Error in {name}: {e}")
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    if stdio_server:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
