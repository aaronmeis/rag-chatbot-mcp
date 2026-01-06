"""
MCP Chunker Server

Document chunking and preprocessing for RAG pipelines.
"""

import json
import logging
import re
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


class ChunkerManager:
    """Manages document chunking operations."""
    
    def __init__(self, default_chunk_size: int = 512, default_overlap: int = 50):
        self.chunk_size = default_chunk_size
        self.overlap = default_overlap
    
    def _split_fixed(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into fixed-size chunks."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk.strip())
            start = end - overlap
        return chunks
    
    def _split_recursive(self, text: str, chunk_size: int, 
                        separators: List[str] = None) -> List[str]:
        """Split text recursively by separators."""
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        
        chunks = []
        
        if len(text) <= chunk_size:
            return [text] if text.strip() else []
        
        for sep in separators:
            if sep in text:
                parts = text.split(sep)
                current_chunk = ""
                
                for part in parts:
                    if len(current_chunk) + len(part) + len(sep) <= chunk_size:
                        current_chunk += (sep if current_chunk else "") + part
                    else:
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())
                        current_chunk = part
                
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                return chunks
        
        # Fallback to fixed splitting
        return self._split_fixed(text, chunk_size, self.overlap)
    
    def _split_sentence(self, text: str, chunk_size: int) -> List[str]:
        """Split text by sentences, grouping to target size."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_paragraph(self, text: str) -> List[str]:
        """Split text by paragraphs."""
        paragraphs = text.split("\n\n")
        return [p.strip() for p in paragraphs if p.strip()]
    
    def chunk_text(self, text: str, strategy: str = "recursive",
                  chunk_size: Optional[int] = None, 
                  overlap: Optional[int] = None) -> dict:
        """Split text using specified strategy."""
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.overlap
        
        if strategy == "fixed":
            chunks = self._split_fixed(text, chunk_size, overlap)
        elif strategy == "recursive":
            chunks = self._split_recursive(text, chunk_size)
        elif strategy == "sentence":
            chunks = self._split_sentence(text, chunk_size)
        elif strategy == "paragraph":
            chunks = self._split_paragraph(text)
        else:
            chunks = self._split_recursive(text, chunk_size)
        
        return {
            "status": "success",
            "strategy": strategy,
            "chunk_size": chunk_size,
            "overlap": overlap,
            "chunks": [
                {
                    "index": i,
                    "text": chunk,
                    "char_count": len(chunk)
                }
                for i, chunk in enumerate(chunks)
            ],
            "total_chunks": len(chunks),
            "total_chars": sum(len(c) for c in chunks)
        }
    
    def chunk_document(self, document: Dict, strategy: str = "recursive") -> dict:
        """Process entire document with metadata."""
        text = document.get("text", "")
        metadata = document.get("metadata", {})
        
        result = self.chunk_text(text, strategy)
        
        # Add document metadata to each chunk
        for chunk in result["chunks"]:
            chunk["metadata"] = {
                **metadata,
                "chunk_index": chunk["index"],
                "total_chunks": result["total_chunks"]
            }
        
        return {
            "status": "success",
            "document_metadata": metadata,
            "strategy": strategy,
            "chunks": result["chunks"],
            "total_chunks": result["total_chunks"]
        }
    
    def set_chunk_size(self, size: int) -> dict:
        """Configure default chunk size."""
        self.chunk_size = size
        return {
            "status": "success",
            "chunk_size": self.chunk_size,
            "message": f"Default chunk size set to {size}"
        }
    
    def set_overlap(self, overlap: int) -> dict:
        """Configure chunk overlap."""
        self.overlap = overlap
        return {
            "status": "success",
            "overlap": self.overlap,
            "message": f"Default overlap set to {overlap}"
        }
    
    def preview_chunks(self, text: str, strategy: str = "recursive") -> dict:
        """Preview chunking without saving."""
        result = self.chunk_text(text, strategy)
        
        # Add preview info
        result["preview"] = True
        result["summary"] = {
            "total_chunks": result["total_chunks"],
            "avg_chunk_size": result["total_chars"] // max(result["total_chunks"], 1),
            "min_chunk_size": min(c["char_count"] for c in result["chunks"]) if result["chunks"] else 0,
            "max_chunk_size": max(c["char_count"] for c in result["chunks"]) if result["chunks"] else 0
        }
        
        return result


# Initialize
app = Server("mcp-chunker") if Server else None
manager = ChunkerManager()

TOOLS = [
    Tool(
        name="chunk_text",
        description="Split text into chunks using specified strategy",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "strategy": {"type": "string", "enum": ["fixed", "recursive", "sentence", "paragraph"]},
                "chunk_size": {"type": "integer"},
                "overlap": {"type": "integer"}
            },
            "required": ["text"]
        }
    ),
    Tool(
        name="chunk_document",
        description="Process document with metadata preservation",
        inputSchema={
            "type": "object",
            "properties": {
                "document": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "metadata": {"type": "object"}
                    }
                },
                "strategy": {"type": "string"}
            },
            "required": ["document"]
        }
    ),
    Tool(
        name="set_chunk_size",
        description="Configure default chunk size",
        inputSchema={
            "type": "object",
            "properties": {
                "size": {"type": "integer"}
            },
            "required": ["size"]
        }
    ),
    Tool(
        name="set_overlap",
        description="Configure chunk overlap",
        inputSchema={
            "type": "object",
            "properties": {
                "overlap": {"type": "integer"}
            },
            "required": ["overlap"]
        }
    ),
    Tool(
        name="preview_chunks",
        description="Preview chunking without saving",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "strategy": {"type": "string"}
            },
            "required": ["text"]
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
            if name == "chunk_text":
                result = manager.chunk_text(**arguments)
            elif name == "chunk_document":
                result = manager.chunk_document(**arguments)
            elif name == "set_chunk_size":
                result = manager.set_chunk_size(**arguments)
            elif name == "set_overlap":
                result = manager.set_overlap(**arguments)
            elif name == "preview_chunks":
                result = manager.preview_chunks(**arguments)
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
