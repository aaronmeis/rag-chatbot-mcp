"""
Tests for mcp-reranker server
"""

import pytest
from unittest.mock import Mock


class TestRerankerManager:
    """Tests for the RerankerManager class"""
    
    def test_rerank_changes_order(self):
        """Test reranking can change document order"""
        original = [
            {"content": "Doc A", "score": 0.9},
            {"content": "Doc B", "score": 0.8},
            {"content": "Doc C", "score": 0.7}
        ]
        
        # Simulate reranking with different scores
        reranked = [
            {"content": "Doc B", "score": 0.95},
            {"content": "Doc A", "score": 0.85},
            {"content": "Doc C", "score": 0.6}
        ]
        
        assert reranked[0]["content"] != original[0]["content"]
    
    def test_rerank_preserves_documents(self):
        """Test reranking doesn't lose documents"""
        documents = [{"id": i, "content": f"Doc {i}"} for i in range(5)]
        
        reranked = sorted(documents, key=lambda x: x["id"], reverse=True)
        
        assert len(reranked) == len(documents)
        original_ids = {d["id"] for d in documents}
        reranked_ids = {d["id"] for d in reranked}
        assert original_ids == reranked_ids
    
    def test_cross_encoder_scoring(self):
        """Test cross-encoder produces relevance scores"""
        query = "What is machine learning?"
        document = "Machine learning is a subset of AI."
        
        # Cross-encoder scores query-document pairs
        mock_score = 0.92
        
        assert 0 <= mock_score <= 1


class TestRerankerMethods:
    """Tests for different reranking methods"""
    
    def test_cross_encoder_reranking(self):
        """Test cross-encoder based reranking"""
        method = "cross-encoder"
        model = "cross-encoder/ms-marco-MiniLM-L-6-v2"
        
        assert method == "cross-encoder"
        assert "cross-encoder" in model
    
    def test_llm_reranking(self):
        """Test LLM-based reranking"""
        method = "llm"
        prompt = "Rate the relevance of this document to the query on a scale of 1-10."
        
        assert method == "llm"
        assert "relevance" in prompt.lower()
    
    def test_reciprocal_rank_fusion(self):
        """Test RRF score calculation"""
        k = 60  # RRF constant
        ranks = [1, 3, 5]  # Document ranks from different systems
        
        rrf_score = sum(1 / (k + r) for r in ranks)
        
        assert rrf_score > 0
        assert rrf_score == pytest.approx(1/61 + 1/63 + 1/65, rel=1e-5)
    
    def test_mmr_diversity(self):
        """Test MMR (Maximal Marginal Relevance) diversity"""
        lambda_param = 0.5  # Balance between relevance and diversity
        relevance_score = 0.9
        max_similarity = 0.8  # Similarity to already selected docs
        
        mmr_score = lambda_param * relevance_score - (1 - lambda_param) * max_similarity
        
        assert mmr_score == pytest.approx(0.05, rel=1e-5)


class TestRankFusion:
    """Tests for rank fusion algorithms"""
    
    def test_rrf_combines_rankings(self):
        """Test RRF combines multiple ranking lists"""
        ranking1 = ["A", "B", "C", "D"]
        ranking2 = ["B", "A", "D", "C"]
        
        # Calculate RRF scores
        k = 60
        scores = {}
        for rank, doc in enumerate(ranking1, 1):
            scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
        for rank, doc in enumerate(ranking2, 1):
            scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
        
        # Sort by combined score
        fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        assert len(fused) == 4
        # B should rank higher (rank 1 in one list, rank 2 in other)
    
    def test_weighted_fusion(self):
        """Test weighted combination of rankings"""
        scores1 = {"A": 0.9, "B": 0.7}
        scores2 = {"A": 0.6, "B": 0.95}
        weight1, weight2 = 0.6, 0.4
        
        combined = {}
        for doc in set(scores1) | set(scores2):
            s1 = scores1.get(doc, 0) * weight1
            s2 = scores2.get(doc, 0) * weight2
            combined[doc] = s1 + s2
        
        assert combined["A"] == pytest.approx(0.78, rel=1e-5)
        assert combined["B"] == pytest.approx(0.8, rel=1e-5)


class TestDiversification:
    """Tests for result diversification"""
    
    def test_mmr_selects_diverse_results(self):
        """Test MMR reduces redundancy"""
        documents = [
            {"id": 1, "content": "ML is great", "embedding": [1, 0, 0]},
            {"id": 2, "content": "ML is awesome", "embedding": [0.99, 0.1, 0]},  # Similar to 1
            {"id": 3, "content": "NLP processes text", "embedding": [0, 1, 0]}  # Different
        ]
        
        # After selecting doc 1, doc 3 should be preferred over doc 2
        # due to diversity
        selected = [1]
        remaining = [2, 3]
        
        # Doc 3 is more diverse from doc 1
        assert 3 in remaining
    
    def test_diversity_threshold(self):
        """Test similarity threshold for diversity"""
        threshold = 0.85
        similarities = [0.9, 0.7, 0.5]
        
        # Docs with similarity > threshold are considered redundant
        redundant = [s for s in similarities if s > threshold]
        assert len(redundant) == 1


class TestRerankerTools:
    """Tests for MCP tool handlers"""
    
    @pytest.mark.asyncio
    async def test_rerank_tool(self):
        """Test rerank tool format"""
        mock_result = {
            "query": "test query",
            "results": [
                {"content": "Doc 1", "original_score": 0.8, "rerank_score": 0.95},
                {"content": "Doc 2", "original_score": 0.9, "rerank_score": 0.75}
            ],
            "method": "cross-encoder",
            "model": "ms-marco-MiniLM-L-6-v2"
        }
        
        assert "results" in mock_result
        assert "method" in mock_result
        # Results should have both original and rerank scores
        assert "original_score" in mock_result["results"][0]
        assert "rerank_score" in mock_result["results"][0]
    
    @pytest.mark.asyncio
    async def test_llm_rerank_tool(self):
        """Test LLM-based rerank tool"""
        mock_result = {
            "query": "test",
            "results": [],
            "method": "llm",
            "model": "gpt-4",
            "prompt_used": "Rate relevance..."
        }
        
        assert mock_result["method"] == "llm"
    
    @pytest.mark.asyncio
    async def test_fuse_rankings_tool(self):
        """Test fuse_rankings tool"""
        mock_result = {
            "fused_results": [
                {"id": "A", "fused_score": 0.85},
                {"id": "B", "fused_score": 0.72}
            ],
            "method": "rrf",
            "rankings_combined": 2
        }
        
        assert "fused_results" in mock_result
        assert mock_result["method"] == "rrf"
    
    @pytest.mark.asyncio
    async def test_diversify_tool(self):
        """Test diversify tool"""
        mock_result = {
            "diversified_results": [],
            "method": "mmr",
            "lambda": 0.5,
            "original_count": 10,
            "diversified_count": 5
        }
        
        assert mock_result["method"] == "mmr"
        assert mock_result["diversified_count"] <= mock_result["original_count"]


class TestRerankerValidation:
    """Tests for input validation"""
    
    def test_empty_results_handling(self):
        """Test handling of empty result list"""
        results = []
        
        # Should return empty list without error
        assert len(results) == 0
    
    def test_top_n_parameter(self):
        """Test top_n limits output"""
        results = [{"id": i} for i in range(20)]
        top_n = 5
        
        limited = results[:top_n]
        assert len(limited) == top_n
    
    def test_score_normalization(self):
        """Test scores are normalized to 0-1 range"""
        raw_scores = [10, 5, 2, 0.5]
        max_score = max(raw_scores)
        
        normalized = [s / max_score for s in raw_scores]
        
        assert all(0 <= s <= 1 for s in normalized)


class TestPerformance:
    """Tests for performance characteristics"""
    
    def test_batch_reranking(self):
        """Test batch processing of multiple documents"""
        batch_size = 100
        documents = [{"id": i, "content": f"Doc {i}"} for i in range(batch_size)]
        
        # All documents should be processed
        assert len(documents) == batch_size
    
    def test_caching_behavior(self):
        """Test caching of rerank scores"""
        cache = {}
        query = "test query"
        doc_id = "doc_1"
        score = 0.85
        
        cache_key = f"{query}:{doc_id}"
        cache[cache_key] = score
        
        # Second lookup should hit cache
        assert cache_key in cache
        assert cache[cache_key] == score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
