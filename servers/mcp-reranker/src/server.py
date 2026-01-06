"""
MCP Reranker Server

Result reranking for improved retrieval quality.
"""

import json
import logging
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


class RerankerManager:
    """Manages reranking operations."""
    
    def __init__(self):
        self.cross_encoder = None
        
    def _compute_relevance(self, query: str, doc: str) -> float:
        """Simple relevance scoring for demo."""
        query_words = set(query.lower().split())
        doc_words = set(doc.lower().split())
        
        if not query_words:
            return 0.0
        
        overlap = len(query_words & doc_words)
        coverage = overlap / len(query_words)
        
        # Bonus for exact phrase match
        if query.lower() in doc.lower():
            coverage += 0.2
        
        return min(coverage, 1.0)
    
    def rerank(self, query: str, documents: List[Dict], 
              top_k: Optional[int] = None) -> dict:
        """Rerank results using cross-encoder scoring."""
        scored_docs = []
        
        for doc in documents:
            text = doc.get("text", doc.get("content", ""))
            score = self._compute_relevance(query, text)
            scored_docs.append({
                **doc,
                "rerank_score": score,
                "original_score": doc.get("score", 0)
            })
        
        # Sort by rerank score
        scored_docs.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        if top_k:
            scored_docs = scored_docs[:top_k]
        
        return {
            "status": "success",
            "query": query,
            "results": scored_docs,
            "count": len(scored_docs),
            "method": "cross_encoder"
        }
    
    def llm_rerank(self, query: str, documents: List[Dict],
                  model: str = "mock") -> dict:
        """Rerank using LLM relevance scoring."""
        # Mock LLM scoring
        scored_docs = []
        
        for doc in documents:
            text = doc.get("text", doc.get("content", ""))
            # Simulate LLM scoring with relevance computation
            base_score = self._compute_relevance(query, text)
            # Add some variance to simulate LLM
            llm_score = base_score + np.random.uniform(-0.1, 0.1)
            llm_score = max(0, min(1, llm_score))
            
            scored_docs.append({
                **doc,
                "llm_score": llm_score,
                "original_score": doc.get("score", 0)
            })
        
        scored_docs.sort(key=lambda x: x["llm_score"], reverse=True)
        
        return {
            "status": "success",
            "query": query,
            "model": model,
            "results": scored_docs,
            "count": len(scored_docs),
            "method": "llm_rerank"
        }
    
    def fuse_rankings(self, rankings: List[List[Dict]], k: int = 60) -> dict:
        """Combine multiple rankings using Reciprocal Rank Fusion."""
        doc_scores = {}
        
        for ranking in rankings:
            for rank, doc in enumerate(ranking):
                doc_id = doc.get("id", str(hash(doc.get("text", ""))))
                
                # RRF formula: 1 / (k + rank)
                rrf_score = 1.0 / (k + rank + 1)
                
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = {
                        "doc": doc,
                        "rrf_score": 0,
                        "appearances": 0
                    }
                
                doc_scores[doc_id]["rrf_score"] += rrf_score
                doc_scores[doc_id]["appearances"] += 1
        
        # Sort by RRF score
        fused_results = [
            {
                **item["doc"],
                "rrf_score": item["rrf_score"],
                "appearances": item["appearances"]
            }
            for item in doc_scores.values()
        ]
        fused_results.sort(key=lambda x: x["rrf_score"], reverse=True)
        
        return {
            "status": "success",
            "num_rankings": len(rankings),
            "k": k,
            "results": fused_results,
            "count": len(fused_results),
            "method": "rrf"
        }
    
    def diversify(self, documents: List[Dict], 
                 lambda_param: float = 0.5, top_k: int = 10) -> dict:
        """Apply MMR-style diversity filtering."""
        if not documents:
            return {"status": "success", "results": [], "count": 0}
        
        selected = [documents[0]]
        remaining = documents[1:]
        
        while len(selected) < top_k and remaining:
            best_doc = None
            best_score = -float('inf')
            
            for doc in remaining:
                doc_text = doc.get("text", "")
                relevance = doc.get("score", doc.get("rerank_score", 0.5))
                
                # Calculate max similarity to selected docs
                max_sim = 0
                for sel_doc in selected:
                    sel_text = sel_doc.get("text", "")
                    # Simple word overlap similarity
                    doc_words = set(doc_text.lower().split())
                    sel_words = set(sel_text.lower().split())
                    if doc_words and sel_words:
                        sim = len(doc_words & sel_words) / len(doc_words | sel_words)
                        max_sim = max(max_sim, sim)
                
                # MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_doc = doc
            
            if best_doc:
                selected.append({**best_doc, "diversity_score": best_score})
                remaining.remove(best_doc)
            else:
                break
        
        return {
            "status": "success",
            "lambda": lambda_param,
            "results": selected,
            "count": len(selected),
            "method": "mmr_diversity"
        }


# Initialize
app = Server("mcp-reranker") if Server else None
manager = RerankerManager()

TOOLS = [
    Tool(
        name="rerank",
        description="Rerank search results using cross-encoder model",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "documents": {"type": "array", "items": {"type": "object"}},
                "top_k": {"type": "integer"}
            },
            "required": ["query", "documents"]
        }
    ),
    Tool(
        name="llm_rerank",
        description="Rerank using LLM relevance scoring",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "documents": {"type": "array", "items": {"type": "object"}},
                "model": {"type": "string"}
            },
            "required": ["query", "documents"]
        }
    ),
    Tool(
        name="fuse_rankings",
        description="Combine multiple rankings using Reciprocal Rank Fusion",
        inputSchema={
            "type": "object",
            "properties": {
                "rankings": {"type": "array", "items": {"type": "array"}},
                "k": {"type": "integer", "default": 60}
            },
            "required": ["rankings"]
        }
    ),
    Tool(
        name="diversify",
        description="Apply diversity filtering to improve result variety",
        inputSchema={
            "type": "object",
            "properties": {
                "documents": {"type": "array", "items": {"type": "object"}},
                "lambda_param": {"type": "number", "default": 0.5},
                "top_k": {"type": "integer", "default": 10}
            },
            "required": ["documents"]
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
            if name == "rerank":
                result = manager.rerank(**arguments)
            elif name == "llm_rerank":
                result = manager.llm_rerank(**arguments)
            elif name == "fuse_rankings":
                result = manager.fuse_rankings(**arguments)
            elif name == "diversify":
                result = manager.diversify(**arguments)
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
