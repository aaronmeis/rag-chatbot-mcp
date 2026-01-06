"""
Tool implementations for MCP VectorStore Server.

This module contains the core business logic for vector database operations,
separated from the MCP server interface.
"""

import logging
from typing import Any, Optional, List, Dict

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    try:
        import numpy as np
    except ImportError:
        np = None

logger = logging.getLogger(__name__)


class VectorStoreTools:
    """Core vector store operations."""

    def __init__(self, backend: str = "chromadb", persist_dir: str = "./chroma_db"):
        """Initialize vector store backend.

        Args:
            backend: Backend type ("chromadb" or "faiss")
            persist_dir: Directory for persistent storage
        """
        self.backend = backend
        self.persist_dir = persist_dir
        self.collections = {}

        if backend == "chromadb" and CHROMADB_AVAILABLE:
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_dir,
                anonymized_telemetry=False
            ))
        elif backend == "faiss" and FAISS_AVAILABLE:
            self.faiss_indexes = {}
            self.faiss_metadata = {}
        else:
            logger.warning(f"Backend {backend} not available, using mock mode")
            self.client = None

    def create_collection(self, name: str, metadata: Optional[Dict] = None,
                         embedding_dimension: int = 1536) -> Dict:
        """Create a new vector collection."""
        if self.backend == "chromadb" and hasattr(self, 'client') and self.client:
            collection = self.client.create_collection(name=name, metadata=metadata or {})
            return {
                "status": "success",
                "collection": name,
                "message": f"Collection '{name}' created successfully"
            }
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            self.faiss_indexes[name] = faiss.IndexFlatL2(embedding_dimension)
            self.faiss_metadata[name] = {"documents": [], "metadatas": [], "ids": []}
            return {
                "status": "success",
                "collection": name,
                "message": f"FAISS collection '{name}' created"
            }
        else:
            self.collections[name] = {
                "documents": [], "embeddings": [], "metadatas": [], "ids": []
            }
            return {
                "status": "success",
                "collection": name,
                "message": f"Mock collection '{name}' created"
            }

    def add_documents(self, collection: str, documents: List[str], embeddings: List[List[float]],
                     metadatas: Optional[List[Dict]] = None, ids: Optional[List[str]] = None) -> Dict:
        """Add documents with embeddings to a collection."""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        if metadatas is None:
            metadatas = [{} for _ in documents]

        if self.backend == "chromadb" and hasattr(self, 'client') and self.client:
            coll = self.client.get_collection(collection)
            coll.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
            return {"status": "success", "added": len(documents), "collection": collection}
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            if collection not in self.faiss_indexes:
                raise ValueError(f"Collection '{collection}' not found")
            embeddings_np = np.array(embeddings).astype('float32')
            self.faiss_indexes[collection].add(embeddings_np)
            self.faiss_metadata[collection]["documents"].extend(documents)
            self.faiss_metadata[collection]["metadatas"].extend(metadatas)
            self.faiss_metadata[collection]["ids"].extend(ids)
            return {"status": "success", "added": len(documents), "collection": collection}
        else:
            if collection not in self.collections:
                self.collections[collection] = {
                    "documents": [], "embeddings": [], "metadatas": [], "ids": []
                }
            self.collections[collection]["documents"].extend(documents)
            self.collections[collection]["embeddings"].extend(embeddings)
            self.collections[collection]["metadatas"].extend(metadatas)
            self.collections[collection]["ids"].extend(ids)
            return {"status": "success", "added": len(documents), "collection": collection, "mode": "mock"}

    def search_similar(self, collection: str, query_embedding: List[float],
                      top_k: int = 10, filter: Optional[Dict] = None) -> Dict:
        """Find similar documents by embedding."""
        if self.backend == "chromadb" and hasattr(self, 'client') and self.client:
            coll = self.client.get_collection(collection)
            results = coll.query(query_embeddings=[query_embedding], n_results=top_k, where=filter)
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
            return {"status": "success", "results": results}
        else:
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

    def delete_documents(self, collection: str, ids: List[str]) -> Dict:
        """Remove documents from a collection."""
        if self.backend == "chromadb" and hasattr(self, 'client') and self.client:
            coll = self.client.get_collection(collection)
            coll.delete(ids=ids)
            return {"status": "success", "deleted": len(ids), "collection": collection}
        else:
            if collection in self.collections:
                for doc_id in ids:
                    if doc_id in self.collections[collection]["ids"]:
                        idx = self.collections[collection]["ids"].index(doc_id)
                        for key in ["documents", "embeddings", "metadatas", "ids"]:
                            self.collections[collection][key].pop(idx)
            return {"status": "success", "deleted": len(ids), "collection": collection, "mode": "mock"}

    def list_collections(self) -> Dict:
        """List all available collections."""
        if self.backend == "chromadb" and hasattr(self, 'client') and self.client:
            collections = self.client.list_collections()
            return {"status": "success", "collections": [c.name for c in collections]}
        elif self.backend == "faiss" and FAISS_AVAILABLE:
            return {"status": "success", "collections": list(self.faiss_indexes.keys())}
        else:
            return {"status": "success", "collections": list(self.collections.keys()), "mode": "mock"}

    def get_collection_stats(self, collection: str) -> Dict:
        """Get statistics for a collection."""
        if self.backend == "chromadb" and hasattr(self, 'client') and self.client:
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
