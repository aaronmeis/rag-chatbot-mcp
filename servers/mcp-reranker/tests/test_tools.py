"""
Tests for Reranker tools.
"""

import pytest
from src.server import RerankerManager


@pytest.fixture
def reranker():
    """Create a reranker instance for testing."""
    return RerankerManager()


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        {"id": "1", "text": "Machine learning is a subset of AI", "score": 0.8},
        {"id": "2", "text": "Deep learning uses neural networks", "score": 0.7},
        {"id": "3", "text": "Natural language processing handles text", "score": 0.6},
        {"id": "4", "text": "Computer vision processes images", "score": 0.5},
    ]


def test_rerank(reranker, sample_documents):
    """Test basic reranking."""
    result = reranker.rerank(
        query="neural networks",
        documents=sample_documents,
        top_k=3
    )

    assert result["status"] == "success"
    assert len(result["results"]) <= 3
    assert all("rerank_score" in doc for doc in result["results"])


def test_llm_rerank(reranker, sample_documents):
    """Test LLM-based reranking."""
    result = reranker.llm_rerank(
        query="machine learning",
        documents=sample_documents,
        model="mock"
    )

    assert result["status"] == "success"
    assert "model" in result
    assert all("llm_score" in doc for doc in result["results"])


def test_fuse_rankings(reranker, sample_documents):
    """Test reciprocal rank fusion."""
    rankings = [
        sample_documents[:3],
        sample_documents[1:4],
        [sample_documents[0], sample_documents[3]]
    ]

    result = reranker.fuse_rankings(rankings, k=60)

    assert result["status"] == "success"
    assert result["num_rankings"] == 3
    assert all("rrf_score" in doc for doc in result["results"])


def test_diversify(reranker, sample_documents):
    """Test diversity filtering."""
    result = reranker.diversify(
        documents=sample_documents,
        lambda_param=0.5,
        top_k=3
    )

    assert result["status"] == "success"
    assert len(result["results"]) <= 3
    assert result["lambda"] == 0.5


def test_empty_documents(reranker):
    """Test reranking with empty document list."""
    result = reranker.rerank(
        query="test",
        documents=[],
        top_k=5
    )

    assert result["status"] == "success"
    assert len(result["results"]) == 0


def test_relevance_computation(reranker):
    """Test relevance scoring."""
    score = reranker._compute_relevance(
        query="machine learning",
        doc="Machine learning is a subset of artificial intelligence"
    )

    assert 0 <= score <= 1
    assert score > 0.3  # Should have good overlap


@pytest.mark.parametrize("lambda_param", [0.0, 0.5, 1.0])
def test_diversity_lambda_values(reranker, sample_documents, lambda_param):
    """Test diversity with different lambda values."""
    result = reranker.diversify(
        documents=sample_documents,
        lambda_param=lambda_param,
        top_k=3
    )

    assert result["status"] == "success"
    assert result["lambda"] == lambda_param


def test_ranking_fusion_multiple_lists(reranker):
    """Test fusion with multiple ranking lists."""
    doc1 = {"id": "1", "text": "Text 1", "score": 0.9}
    doc2 = {"id": "2", "text": "Text 2", "score": 0.8}
    doc3 = {"id": "3", "text": "Text 3", "score": 0.7}

    rankings = [
        [doc1, doc2, doc3],
        [doc2, doc1, doc3],
        [doc3, doc2, doc1]
    ]

    result = reranker.fuse_rankings(rankings)

    assert result["status"] == "success"
    # Document 2 appears highly in all rankings
    assert len(result["results"]) == 3


def test_rerank_preserves_metadata(reranker):
    """Test that reranking preserves document metadata."""
    docs = [
        {"id": "1", "text": "Test", "score": 0.5, "metadata": {"source": "A"}},
        {"id": "2", "text": "Test two", "score": 0.6, "metadata": {"source": "B"}},
    ]

    result = reranker.rerank(query="test", documents=docs)

    assert all("metadata" in doc for doc in result["results"])
