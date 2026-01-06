"""
MCP VectorStore Server

Vector database operations for RAG pipelines.
Supports ChromaDB and FAISS backends.
"""

import json
import logging
import os
from typing import Any, Optional

# Initialize logger early (before imports that may use it)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    # Fallback for development
    Server = None
    stdio_server = None

# Vector store imports
CHROMADB_AVAILABLE = False
CHROMADB_HTTP_AVAILABLE = False

try:
    # Try to import HttpClient (works with chromadb-client or full chromadb)
    # Note: May have issues on Python 3.14+ due to pydantic v1 compatibility
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        try:
            from chromadb import HttpClient
            CHROMADB_HTTP_AVAILABLE = True
        except (ImportError, Exception) as e:
            logger.debug(f"HttpClient import failed: {e}")
            CHROMADB_HTTP_AVAILABLE = False
        
        # Try full chromadb for local client (may fail on Python 3.14+)
        try:
            import chromadb
            from chromadb.config import Settings
            CHROMADB_AVAILABLE = True
        except (ImportError, Exception) as e:
            logger.debug(f"Local chromadb import failed: {e}")
            CHROMADB_AVAILABLE = False
            # If we have HttpClient, we can still use Docker mode
            if CHROMADB_HTTP_AVAILABLE:
                logger.info("Using ChromaDB HTTP client only (Docker mode)")
except Exception as e:
    logger.debug(f"ChromaDB import error: {e}")
    CHROMADB_AVAILABLE = False
    CHROMADB_HTTP_AVAILABLE = False

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class VectorStoreManager:
    """Manages vector store operations across different backends."""
    
    def __init__(self, backend: str = "chromadb", persist_dir: str = "./chroma_db", 
                 chroma_host: str = None, chroma_port: int = 8000):
        self.backend = backend
        self.persist_dir = persist_dir
        self.collections = {}
        self.chroma_host = chroma_host or os.getenv("CHROMA_HOST", "localhost")
        self.chroma_port = chroma_port or int(os.getenv("CHROMA_PORT", "8000"))
        
        if backend == "chromadb":
            # Try HTTP client first (for Docker) - this works even if local chromadb fails
            if CHROMADB_HTTP_AVAILABLE:
                try:
                    # Try to connect to ChromaDB server
                    self.client = HttpClient(host=self.chroma_host, port=self.chroma_port)
                    # Test connection by listing collections (lightweight operation)
                    try:
                        self.client.list_collections()
                        logger.info(f"✅ Connected to ChromaDB server at {self.chroma_host}:{self.chroma_port}")
                    except Exception as e:
                        # Server exists but connection failed
                        logger.warning(f"ChromaDB server at {self.chroma_host}:{self.chroma_port} not responding: {e}")
                        logger.info("Will try to use server anyway, or fall back to mock mode")
                        # Keep the client - it might work for operations even if list_collections fails
                except Exception as e:
                    # HttpClient creation failed
                    logger.warning(f"ChromaDB HTTP client creation failed: {e}")
                    self.client = None
            elif CHROMADB_AVAILABLE:
                # Use local client (only if HTTP client not available)
                try:
                    self.client = chromadb.Client(Settings(
                        chroma_db_impl="duckdb+parquet",
                        persist_directory=persist_dir,
                        anonymized_telemetry=False
                    ))
                    logger.info("Using local ChromaDB client")
                except Exception as e:
                    logger.warning(f"Local ChromaDB client failed: {e}")
                    self.client = None
            else:
                self.client = None
                logger.warning("ChromaDB not available, using mock mode")
        elif backend == "faiss" and FAISS_AVAILABLE:
            self.faiss_indexes = {}
            self.faiss_metadata = {}
        else:
            logger.warning(f"Backend {backend} not available, using mock mode")
            self.client = None
    
    def create_collection(self, name: str, metadata: Optional[dict] = None, 
                         embedding_dimension: int = 1536) -> dict:
        """Create a new vector collection."""
        if self.backend == "chromadb" and self.client:
            collection = self.client.create_collection(
                name=name,
                metadata=metadata or {}
            )
            return {
                "status": "success",
                "collection": name,
                "message": f"Collection '{name}' created successfully"
            }
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            self.faiss_indexes[name] = faiss.IndexFlatL2(embedding_dimension)
            self.faiss_metadata[name] = {
                "documents": [],
                "metadatas": [],
                "ids": []
            }
            return {
                "status": "success",
                "collection": name,
                "message": f"FAISS collection '{name}' created"
            }
        else:
            # Mock mode
            self.collections[name] = {
                "documents": [],
                "embeddings": [],
                "metadatas": [],
                "ids": []
            }
            return {
                "status": "success",
                "collection": name,
                "message": f"Mock collection '{name}' created"
            }
    
    def add_documents(self, collection: str, documents: list, embeddings: list,
                     metadatas: Optional[list] = None, ids: Optional[list] = None) -> dict:
        """Add documents with embeddings to a collection."""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        if self.backend == "chromadb" and self.client:
            coll = self.client.get_collection(collection)
            coll.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            return {
                "status": "success",
                "added": len(documents),
                "collection": collection
            }
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            if collection not in self.faiss_indexes:
                raise ValueError(f"Collection '{collection}' not found")
            
            embeddings_np = np.array(embeddings).astype('float32')
            self.faiss_indexes[collection].add(embeddings_np)
            self.faiss_metadata[collection]["documents"].extend(documents)
            self.faiss_metadata[collection]["metadatas"].extend(metadatas)
            self.faiss_metadata[collection]["ids"].extend(ids)
            
            return {
                "status": "success",
                "added": len(documents),
                "collection": collection
            }
        else:
            # Mock mode
            if collection not in self.collections:
                self.collections[collection] = {
                    "documents": [],
                    "embeddings": [],
                    "metadatas": [],
                    "ids": []
                }
            self.collections[collection]["documents"].extend(documents)
            self.collections[collection]["embeddings"].extend(embeddings)
            self.collections[collection]["metadatas"].extend(metadatas)
            self.collections[collection]["ids"].extend(ids)
            
            return {
                "status": "success",
                "added": len(documents),
                "collection": collection,
                "mode": "mock"
            }
    
    def search_similar(self, collection: str, query_embedding: list, 
                      top_k: int = 10, filter: Optional[dict] = None) -> dict:
        """Find similar documents by embedding."""
        if self.backend == "chromadb" and self.client:
            coll = self.client.get_collection(collection)
            results = coll.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter
            )
            return {
                "status": "success",
                "results": [
                    {
                        "id": results["ids"][0][i],
                        "document": results["documents"][0][i] if results["documents"] else None,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0
                    }
                    for i in range(len(results["ids"][0]))
                ]
            }
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            if collection not in self.faiss_indexes:
                raise ValueError(f"Collection '{collection}' not found")
            
            query_np = np.array([query_embedding]).astype('float32')
            distances, indices = self.faiss_indexes[collection].search(query_np, top_k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.faiss_metadata[collection]["documents"]):
                    results.append({
                        "id": self.faiss_metadata[collection]["ids"][idx],
                        "document": self.faiss_metadata[collection]["documents"][idx],
                        "metadata": self.faiss_metadata[collection]["metadatas"][idx],
                        "distance": float(distances[0][i])
                    })
            
            return {
                "status": "success",
                "results": results
            }
        else:
            # Mock mode - return mock results
            if collection in self.collections:
                docs = self.collections[collection]["documents"][:top_k]
                return {
                    "status": "success",
                    "results": [
                        {
                            "id": f"doc_{i}",
                            "document": doc,
                            "metadata": {},
                            "distance": 0.1 * (i + 1)
                        }
                        for i, doc in enumerate(docs)
                    ],
                    "mode": "mock"
                }
            return {"status": "success", "results": [], "mode": "mock"}
    
    def delete_documents(self, collection: str, ids: list) -> dict:
        """Remove documents from a collection."""
        if self.backend == "chromadb" and self.client:
            coll = self.client.get_collection(collection)
            coll.delete(ids=ids)
            return {
                "status": "success",
                "deleted": len(ids),
                "collection": collection
            }
        else:
            # Mock mode
            if collection in self.collections:
                for doc_id in ids:
                    if doc_id in self.collections[collection]["ids"]:
                        idx = self.collections[collection]["ids"].index(doc_id)
                        for key in ["documents", "embeddings", "metadatas", "ids"]:
                            self.collections[collection][key].pop(idx)
            return {
                "status": "success",
                "deleted": len(ids),
                "collection": collection,
                "mode": "mock"
            }
    
    def list_collections(self) -> dict:
        """List all available collections."""
        if self.backend == "chromadb" and self.client:
            collections = self.client.list_collections()
            return {
                "status": "success",
                "collections": [c.name for c in collections]
            }
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            return {
                "status": "success",
                "collections": list(self.faiss_indexes.keys())
            }
        else:
            return {
                "status": "success",
                "collections": list(self.collections.keys()),
                "mode": "mock"
            }
    
    def get_collection_stats(self, collection: str) -> dict:
        """Get statistics for a collection."""
        if self.backend == "chromadb" and self.client:
            coll = self.client.get_collection(collection)
            return {
                "status": "success",
                "collection": collection,
                "count": coll.count(),
                "metadata": coll.metadata
            }
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            if collection not in self.faiss_indexes:
                raise ValueError(f"Collection '{collection}' not found")
            return {
                "status": "success",
                "collection": collection,
                "count": self.faiss_indexes[collection].ntotal
            }
        else:
            if collection in self.collections:
                return {
                    "status": "success",
                    "collection": collection,
                    "count": len(self.collections[collection]["documents"]),
                    "mode": "mock"
                }
            return {"status": "error", "message": f"Collection '{collection}' not found"}


# Initialize server and manager
app = Server("mcp-vectorstore") if Server else None
manager = VectorStoreManager(
    backend=os.getenv("VECTORSTORE_BACKEND", "chromadb"),
    persist_dir=os.getenv("VECTORSTORE_PATH", "./chroma_db"),
    chroma_host=os.getenv("CHROMA_HOST", "localhost"),
    chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
)


# Tool definitions
TOOLS = [
    Tool(
        name="create_collection",
        description="Create a new vector collection for storing embeddings",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Collection name"},
                "metadata": {"type": "object", "description": "Collection metadata"},
                "embedding_dimension": {"type": "integer", "default": 1536}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="add_documents",
        description="Add documents with embeddings to a collection",
        inputSchema={
            "type": "object",
            "properties": {
                "collection": {"type": "string", "description": "Collection name"},
                "documents": {"type": "array", "items": {"type": "string"}},
                "embeddings": {"type": "array", "items": {"type": "array"}},
                "metadatas": {"type": "array", "items": {"type": "object"}},
                "ids": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["collection", "documents", "embeddings"]
        }
    ),
    Tool(
        name="search_similar",
        description="Find similar documents by embedding vector",
        inputSchema={
            "type": "object",
            "properties": {
                "collection": {"type": "string", "description": "Collection name"},
                "query_embedding": {"type": "array", "items": {"type": "number"}},
                "top_k": {"type": "integer", "default": 10},
                "filter": {"type": "object", "description": "Metadata filter"}
            },
            "required": ["collection", "query_embedding"]
        }
    ),
    Tool(
        name="delete_documents",
        description="Remove documents from a collection by ID",
        inputSchema={
            "type": "object",
            "properties": {
                "collection": {"type": "string"},
                "ids": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["collection", "ids"]
        }
    ),
    Tool(
        name="list_collections",
        description="List all available vector collections",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="get_collection_stats",
        description="Get statistics for a vector collection",
        inputSchema={
            "type": "object",
            "properties": {
                "collection": {"type": "string"}
            },
            "required": ["collection"]
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
            if name == "create_collection":
                result = manager.create_collection(
                    name=arguments["name"],
                    metadata=arguments.get("metadata"),
                    embedding_dimension=arguments.get("embedding_dimension", 1536)
                )
            elif name == "add_documents":
                result = manager.add_documents(
                    collection=arguments["collection"],
                    documents=arguments["documents"],
                    embeddings=arguments["embeddings"],
                    metadatas=arguments.get("metadatas"),
                    ids=arguments.get("ids")
                )
            elif name == "search_similar":
                result = manager.search_similar(
                    collection=arguments["collection"],
                    query_embedding=arguments["query_embedding"],
                    top_k=arguments.get("top_k", 10),
                    filter=arguments.get("filter")
                )
            elif name == "delete_documents":
                result = manager.delete_documents(
                    collection=arguments["collection"],
                    ids=arguments["ids"]
                )
            elif name == "list_collections":
                result = manager.list_collections()
            elif name == "get_collection_stats":
                result = manager.get_collection_stats(
                    collection=arguments["collection"]
                )
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
    else:
        logger.info("MCP SDK not available, running in mock mode")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
