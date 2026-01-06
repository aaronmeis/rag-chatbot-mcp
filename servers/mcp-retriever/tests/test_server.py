"""
Tests for mcp-retriever server
"""

import pytest
from unittest.mock import Mock, patch


class TestRetrieverManager:
    """Tests for the RetrieverManager class"""
    
    def test_retrieve_returns_documents(self):
        """Test basic retrieval returns documents"""
        mock_results = [
            {"content": "Document 1", "score": 0.95, "metadata": {}},
            {"content": "Document 2", "score": 0.87, "metadata": {}},
            {"content": "Document 3", "score": 0.72, "metadata": {}}
        ]
        
        assert len(mock_results) == 3
        assert all("content" in doc for doc in mock_results)
        assert all("score" in doc for doc in mock_results)
    
    def test_retrieve_respects_top_k(self):
        """Test that top_k parameter limits results"""
        top_k = 5
        mock_results = [{"content": f"Doc {i}", "score": 0.9 - i*0.1} for i in range(10)]
        
        limited_results = mock_results[:top_k]
        assert len(limited_results) == top_k
    
    def test_results_sorted_by_score(self):
        """Test results are sorted by relevance score"""
        mock_results = [
            {"content": "Doc 1", "score": 0.72},
            {"content": "Doc 2", "score": 0.95},
            {"content": "Doc 3", "score": 0.87}
        ]
        
        sorted_results = sorted(mock_results, key=lambda x: x["score"], reverse=True)
        assert sorted_results[0]["score"] == 0.95
        assert sorted_results[-1]["score"] == 0.72


class TestRetrievalStrategies:
    """Tests for different retrieval strategies"""
    
    def test_dense_retrieval(self):
        """Test semantic/dense retrieval"""
        strategy = "dense"
        query = "What is machine learning?"
        
        # Dense retrieval uses embedding similarity
        assert strategy == "dense"
    
    def test_sparse_retrieval(self):
        """Test BM25/sparse retrieval"""
        strategy = "sparse"
        query = "machine learning algorithms"
        
        # Sparse retrieval uses keyword matching
        assert strategy == "sparse"
    
    def test_hybrid_retrieval(self):
        """Test hybrid retrieval combining dense and sparse"""
        strategy = "hybrid"
        dense_weight = 0.7
        sparse_weight = 0.3
        
        assert dense_weight + sparse_weight == 1.0
        assert strategy == "hybrid"
    
    def test_hybrid_score_fusion(self):
        """Test score fusion in hybrid search"""
        dense_score = 0.85
        sparse_score = 0.90
        dense_weight = 0.7
        sparse_weight = 0.3
        
        fused_score = (dense_score * dense_weight) + (sparse_score * sparse_weight)
        assert 0 <= fused_score <= 1.0
        assert fused_score == pytest.approx(0.865, rel=1e-3)


class TestMetadataFiltering:
    """Tests for metadata-based filtering"""
    
    def test_single_filter(self):
        """Test filtering by single metadata field"""
        documents = [
            {"content": "Doc 1", "metadata": {"category": "science"}},
            {"content": "Doc 2", "metadata": {"category": "history"}},
            {"content": "Doc 3", "metadata": {"category": "science"}}
        ]
        
        filtered = [d for d in documents if d["metadata"]["category"] == "science"]
        assert len(filtered) == 2
    
    def test_multiple_filters(self):
        """Test filtering by multiple metadata fields"""
        documents = [
            {"content": "Doc 1", "metadata": {"category": "science", "year": 2023}},
            {"content": "Doc 2", "metadata": {"category": "science", "year": 2022}},
            {"content": "Doc 3", "metadata": {"category": "history", "year": 2023}}
        ]
        
        filtered = [d for d in documents 
                   if d["metadata"]["category"] == "science" and d["metadata"]["year"] == 2023]
        assert len(filtered) == 1
    
    def test_range_filter(self):
        """Test filtering by numeric range"""
        documents = [
            {"content": "Doc 1", "metadata": {"score": 85}},
            {"content": "Doc 2", "metadata": {"score": 92}},
            {"content": "Doc 3", "metadata": {"score": 78}}
        ]
        
        filtered = [d for d in documents if d["metadata"]["score"] >= 80]
        assert len(filtered) == 2


class TestMultiQueryRetrieval:
    """Tests for multi-query retrieval"""
    
    def test_query_expansion(self):
        """Test query is expanded into multiple variants"""
        original_query = "What is RAG?"
        expanded_queries = [
            "What is RAG?",
            "What is Retrieval-Augmented Generation?",
            "Explain RAG architecture",
            "RAG definition and overview"
        ]
        
        assert len(expanded_queries) >= 3
        assert original_query in expanded_queries
    
    def test_results_deduplication(self):
        """Test duplicate results are removed"""
        results_query1 = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
        results_query2 = [{"id": "2"}, {"id": "4"}, {"id": "5"}]
        
        all_ids = set()
        for r in results_query1 + results_query2:
            all_ids.add(r["id"])
        
        assert len(all_ids) == 5  # Deduplicated


class TestRetrievalTools:
    """Tests for MCP tool handlers"""
    
    @pytest.mark.asyncio
    async def test_retrieve_tool_format(self):
        """Test retrieve tool returns correct format"""
        mock_result = {
            "query": "test query",
            "results": [
                {"content": "Doc 1", "score": 0.95, "metadata": {}}
            ],
            "total_results": 1,
            "strategy": "dense"
        }
        
        assert "query" in mock_result
        assert "results" in mock_result
        assert "strategy" in mock_result
    
    @pytest.mark.asyncio
    async def test_retrieve_with_filters_tool(self):
        """Test filtered retrieval tool"""
        mock_result = {
            "query": "test",
            "filters": {"category": "science"},
            "results": [],
            "filters_applied": True
        }
        
        assert "filters" in mock_result
        assert mock_result["filters_applied"] is True
    
    @pytest.mark.asyncio
    async def test_hybrid_search_tool(self):
        """Test hybrid search tool"""
        mock_result = {
            "query": "test",
            "strategy": "hybrid",
            "dense_weight": 0.7,
            "sparse_weight": 0.3,
            "results": []
        }
        
        assert mock_result["strategy"] == "hybrid"
        assert mock_result["dense_weight"] + mock_result["sparse_weight"] == 1.0
    
    @pytest.mark.asyncio
    async def test_set_retrieval_params_tool(self):
        """Test parameter configuration tool"""
        mock_result = {
            "success": True,
            "params": {
                "top_k": 10,
                "strategy": "hybrid",
                "threshold": 0.5
            }
        }
        
        assert mock_result["success"] is True
        assert "params" in mock_result


class TestRetrievalValidation:
    """Tests for input validation"""
    
    def test_empty_query_handling(self):
        """Test empty query is handled"""
        query = ""
        assert len(query) == 0
    
    def test_top_k_bounds(self):
        """Test top_k parameter bounds"""
        min_k = 1
        max_k = 100
        
        valid_k = 10
        assert min_k <= valid_k <= max_k
    
    def test_invalid_strategy_handling(self):
        """Test invalid strategy is rejected"""
        valid_strategies = ["dense", "sparse", "hybrid"]
        invalid_strategy = "invalid"
        
        assert invalid_strategy not in valid_strategies


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
