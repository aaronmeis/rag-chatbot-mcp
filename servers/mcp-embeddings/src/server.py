"""
MCP Embeddings Server

Generate embeddings using various models (OpenAI, local transformers).
"""

import json
import logging
import os
from typing import Any, Optional, List

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    Server = None
    stdio_server = None

# Optional imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manages embedding generation across different providers."""
    
    MODELS = {
        "text-embedding-3-small": {"provider": "openai", "dimensions": 1536},
        "text-embedding-3-large": {"provider": "openai", "dimensions": 3072},
        "text-embedding-ada-002": {"provider": "openai", "dimensions": 1536},
        "all-MiniLM-L6-v2": {"provider": "local", "dimensions": 384},
        "all-mpnet-base-v2": {"provider": "local", "dimensions": 768},
        "e5-large-v2": {"provider": "local", "dimensions": 1024}
    }
    
    def __init__(self, default_model: str = "text-embedding-3-small"):
        self.current_model = default_model
        self.openai_client = None
        self.local_model = None
        self.cache = {}
        
        # Initialize OpenAI if available
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI()
        
    def _get_model_info(self, model: str) -> dict:
        """Get model configuration."""
        return self.MODELS.get(model, {"provider": "mock", "dimensions": 1536})
    
    def _load_local_model(self, model: str):
        """Load a local sentence transformer model."""
        if TRANSFORMERS_AVAILABLE:
            self.local_model = SentenceTransformer(model)
        else:
            logger.warning("sentence-transformers not available")
    
    def embed_text(self, text: str, model: Optional[str] = None) -> dict:
        """Generate embedding for single text."""
        model = model or self.current_model
        model_info = self._get_model_info(model)
        
        # Check cache
        cache_key = f"{model}:{hash(text)}"
        if cache_key in self.cache:
            return {
                "status": "success",
                "embedding": self.cache[cache_key],
                "model": model,
                "dimensions": len(self.cache[cache_key]),
                "cached": True
            }
        
        try:
            if model_info["provider"] == "openai" and self.openai_client:
                response = self.openai_client.embeddings.create(
                    input=text,
                    model=model
                )
                embedding = response.data[0].embedding
            elif model_info["provider"] == "local" and TRANSFORMERS_AVAILABLE:
                if self.local_model is None or self.local_model._first_module().auto_model.name_or_path != model:
                    self._load_local_model(model)
                embedding = self.local_model.encode(text).tolist()
            else:
                # Mock embedding
                np.random.seed(hash(text) % (2**32))
                embedding = np.random.randn(model_info["dimensions"]).tolist()
            
            # Cache result
            self.cache[cache_key] = embedding
            
            return {
                "status": "success",
                "embedding": embedding,
                "model": model,
                "dimensions": len(embedding)
            }
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return {"status": "error", "message": str(e)}
    
    def embed_batch(self, texts: List[str], model: Optional[str] = None) -> dict:
        """Generate embeddings for multiple texts."""
        model = model or self.current_model
        model_info = self._get_model_info(model)
        
        try:
            if model_info["provider"] == "openai" and self.openai_client:
                response = self.openai_client.embeddings.create(
                    input=texts,
                    model=model
                )
                embeddings = [item.embedding for item in response.data]
            elif model_info["provider"] == "local" and TRANSFORMERS_AVAILABLE:
                if self.local_model is None:
                    self._load_local_model(model)
                embeddings = self.local_model.encode(texts).tolist()
            else:
                # Mock embeddings
                embeddings = []
                for text in texts:
                    np.random.seed(hash(text) % (2**32))
                    embeddings.append(np.random.randn(model_info["dimensions"]).tolist())
            
            return {
                "status": "success",
                "embeddings": embeddings,
                "model": model,
                "count": len(embeddings),
                "dimensions": model_info["dimensions"]
            }
        except Exception as e:
            logger.error(f"Error in batch embedding: {e}")
            return {"status": "error", "message": str(e)}
    
    def set_model(self, model: str, provider: Optional[str] = None) -> dict:
        """Set the default embedding model."""
        if model in self.MODELS:
            self.current_model = model
            return {
                "status": "success",
                "model": model,
                "provider": self.MODELS[model]["provider"],
                "dimensions": self.MODELS[model]["dimensions"]
            }
        elif provider:
            # Custom model
            self.current_model = model
            self.MODELS[model] = {"provider": provider, "dimensions": 1536}
            return {
                "status": "success",
                "model": model,
                "provider": provider,
                "message": "Custom model configured"
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown model: {model}. Available: {list(self.MODELS.keys())}"
            }
    
    def get_model_info(self) -> dict:
        """Get current model information."""
        info = self._get_model_info(self.current_model)
        return {
            "status": "success",
            "current_model": self.current_model,
            "provider": info["provider"],
            "dimensions": info["dimensions"],
            "available_models": list(self.MODELS.keys()),
            "openai_available": self.openai_client is not None,
            "local_available": TRANSFORMERS_AVAILABLE
        }


# Initialize
app = Server("mcp-embeddings") if Server else None
manager = EmbeddingManager(
    default_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
)

TOOLS = [
    Tool(
        name="embed_text",
        description="Generate embedding vector for a single text",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to embed"},
                "model": {"type": "string", "description": "Model to use"}
            },
            "required": ["text"]
        }
    ),
    Tool(
        name="embed_batch",
        description="Generate embeddings for multiple texts efficiently",
        inputSchema={
            "type": "object",
            "properties": {
                "texts": {"type": "array", "items": {"type": "string"}},
                "model": {"type": "string"}
            },
            "required": ["texts"]
        }
    ),
    Tool(
        name="set_model",
        description="Configure the default embedding model",
        inputSchema={
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "provider": {"type": "string"}
            },
            "required": ["model"]
        }
    ),
    Tool(
        name="get_model_info",
        description="Get current embedding model configuration",
        inputSchema={"type": "object", "properties": {}}
    )
]

if app:
    @app.list_tools()
    async def list_tools():
        return TOOLS

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "embed_text":
                result = manager.embed_text(
                    text=arguments["text"],
                    model=arguments.get("model")
                )
            elif name == "embed_batch":
                result = manager.embed_batch(
                    texts=arguments["texts"],
                    model=arguments.get("model")
                )
            elif name == "set_model":
                result = manager.set_model(
                    model=arguments["model"],
                    provider=arguments.get("provider")
                )
            elif name == "get_model_info":
                result = manager.get_model_info()
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
