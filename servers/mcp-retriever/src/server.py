"""
MCP Retriever Server

Document retrieval with dense, sparse, and hybrid search strategies.
"""

import json
import logging
import os
from typing import Any, Optional, List, Dict

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    Server = None
    stdio_server = None

import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetrieverManager:
    """Manages document retrieval operations."""
    
    def __init__(self):
        self.default_top_k = 10
        self.similarity_threshold = 0.0
        self.vectorstore_url = os.getenv("VECTORSTORE_URL", "http://localhost:8000")
        self.embeddings_url = os.getenv("EMBEDDINGS_URL", "http://localhost:8001")
        
        # Mock data for development
        self.mock_documents = [
            {"id": "1", "text": "Machine learning is a subset of AI.", "score": 0.95},
            {"id": "2", "text": "Deep learning uses neural networks.", "score": 0.90},
            {"id": "3", "text": "Natural language processing handles text.", "score": 0.85},
            {"id": "4", "text": "Computer vision processes images.", "score": 0.80},
            {"id": "5", "text": "Reinforcement learning learns from rewards.", "score": 0.75},
        ]
    
    def _compute_similarity(self, query: str, doc: str) -> float:
        """Simple similarity computation for demo."""
        query_words = set(query.lower().split())
        doc_words = set(doc.lower().split())
        if not query_words or not doc_words:
            return 0.0
        overlap = len(query_words & doc_words)
        return overlap / len(query_words)
    
    def retrieve(self, query: str, collection: str, top_k: Optional[int] = None) -> dict:
        """Basic retrieval with top-k results."""
        top_k = top_k or self.default_top_k
        
        # Score documents
        results = []
        for doc in self.mock_documents:
            score = self._compute_similarity(query, doc["text"])
            if score >= self.similarity_threshold:
                results.append({
                    "id": doc["id"],
                    "text": doc["text"],
                    "score": score,
                    "metadata": {"collection": collection}
                })
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:top_k]
        
        return {
            "status": "success",
            "query": query,
            "collection": collection,
            "results": results,
            "count": len(results)
        }
    
    def retrieve_with_filters(self, query: str, collection: str, 
                             filters: Dict, top_k: Optional[int] = None) -> dict:
        """Retrieval with metadata filtering."""
        top_k = top_k or self.default_top_k
        
        # Get base results
        base_results = self.retrieve(query, collection, top_k * 2)
        
        # Apply filters (mock implementation)
        filtered = []
        for result in base_results["results"]:
            # In real implementation, filter by metadata
            filtered.append(result)
        
        return {
            "status": "success",
            "query": query,
            "collection": collection,
            "filters": filters,
            "results": filtered[:top_k],
            "count": len(filtered[:top_k])
        }
    
    def hybrid_search(self, query: str, collection: str, 
                     alpha: float = 0.5, top_k: Optional[int] = None) -> dict:
        """Combined dense + sparse search."""
        top_k = top_k or self.default_top_k
        
        # Get dense results (semantic)
        dense_results = self.retrieve(query, collection, top_k)["results"]
        
        # Simulate sparse results (BM25-style)
        sparse_results = []
        for doc in self.mock_documents:
            query_terms = query.lower().split()
            doc_terms = doc["text"].lower().split()
            
            # Simple term frequency
            tf_score = sum(1 for t in query_terms if t in doc_terms)
            sparse_results.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": tf_score / len(query_terms) if query_terms else 0
            })
        
        # Combine scores
        combined = {}
        for r in dense_results:
            combined[r["id"]] = {"dense": r["score"], "sparse": 0, "text": r["text"]}
        for r in sparse_results:
            if r["id"] in combined:
                combined[r["id"]]["sparse"] = r["score"]
            else:
                combined[r["id"]] = {"dense": 0, "sparse": r["score"], "text": r["text"]}
        
        # Calculate hybrid score
        results = []
        for doc_id, scores in combined.items():
            hybrid_score = alpha * scores["dense"] + (1 - alpha) * scores["sparse"]
            results.append({
                "id": doc_id,
                "text": scores["text"],
                "score": hybrid_score,
                "dense_score": scores["dense"],
                "sparse_score": scores["sparse"]
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "status": "success",
            "query": query,
            "collection": collection,
            "alpha": alpha,
            "results": results[:top_k],
            "count": len(results[:top_k])
        }
    
    def multi_query_retrieve(self, query: str, collection: str, 
                            num_queries: int = 3, top_k: Optional[int] = None) -> dict:
        """Query expansion retrieval."""
        top_k = top_k or self.default_top_k
        
        # Generate query variants (mock)
        query_variants = [
            query,
            f"What is {query}?",
            f"Explain {query}"
        ][:num_queries]
        
        # Retrieve for each variant
        all_results = {}
        for q in query_variants:
            results = self.retrieve(q, collection, top_k)["results"]
            for r in results:
                if r["id"] not in all_results:
                    all_results[r["id"]] = r
                    all_results[r["id"]]["query_matches"] = 1
                else:
                    all_results[r["id"]]["query_matches"] += 1
                    all_results[r["id"]]["score"] = max(
                        all_results[r["id"]]["score"], 
                        r["score"]
                    )
        
        # Rank by match count and score
        results = list(all_results.values())
        results.sort(key=lambda x: (x["query_matches"], x["score"]), reverse=True)
        
        return {
            "status": "success",
            "original_query": query,
            "expanded_queries": query_variants,
            "collection": collection,
            "results": results[:top_k],
            "count": len(results[:top_k])
        }
    
    def set_retrieval_params(self, default_top_k: Optional[int] = None,
                            similarity_threshold: Optional[float] = None) -> dict:
        """Configure retrieval parameters."""
        if default_top_k is not None:
            self.default_top_k = default_top_k
        if similarity_threshold is not None:
            self.similarity_threshold = similarity_threshold
        
        return {
            "status": "success",
            "default_top_k": self.default_top_k,
            "similarity_threshold": self.similarity_threshold
        }


# Initialize
app = Server("mcp-retriever") if Server else None
manager = RetrieverManager()

TOOLS = [
    Tool(
        name="retrieve",
        description="Basic document retrieval with semantic search",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "collection": {"type": "string"},
                "top_k": {"type": "integer", "default": 10}
            },
            "required": ["query", "collection"]
        }
    ),
    Tool(
        name="retrieve_with_filters",
        description="Retrieve documents with metadata filtering",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "collection": {"type": "string"},
                "filters": {"type": "object"},
                "top_k": {"type": "integer"}
            },
            "required": ["query", "collection", "filters"]
        }
    ),
    Tool(
        name="hybrid_search",
        description="Combined dense (semantic) + sparse (keyword) search",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "collection": {"type": "string"},
                "alpha": {"type": "number", "minimum": 0, "maximum": 1},
                "top_k": {"type": "integer"}
            },
            "required": ["query", "collection"]
        }
    ),
    Tool(
        name="multi_query_retrieve",
        description="Retrieval with query expansion for better recall",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "collection": {"type": "string"},
                "num_queries": {"type": "integer", "default": 3},
                "top_k": {"type": "integer"}
            },
            "required": ["query", "collection"]
        }
    ),
    Tool(
        name="set_retrieval_params",
        description="Configure default retrieval parameters",
        inputSchema={
            "type": "object",
            "properties": {
                "default_top_k": {"type": "integer"},
                "similarity_threshold": {"type": "number"}
            }
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
            if name == "retrieve":
                result = manager.retrieve(**arguments)
            elif name == "retrieve_with_filters":
                result = manager.retrieve_with_filters(**arguments)
            elif name == "hybrid_search":
                result = manager.hybrid_search(**arguments)
            elif name == "multi_query_retrieve":
                result = manager.multi_query_retrieve(**arguments)
            elif name == "set_retrieval_params":
                result = manager.set_retrieval_params(**arguments)
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
