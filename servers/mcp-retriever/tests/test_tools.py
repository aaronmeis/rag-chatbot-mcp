"""
Tests for Retriever tools.
"""

import pytest
from src.server import RetrieverManager


@pytest.fixture
def retriever():
    """Create a retriever instance for testing."""
    return RetrieverManager()


def test_basic_retrieve(retriever):
    """Test basic retrieval."""
    result = retriever.retrieve(
        query="machine learning",
        collection="test_collection",
        top_k=5
    )

    assert result["status"] == "success"
    assert "results" in result
    assert result["count"] >= 0


def test_retrieve_with_filters(retriever):
    """Test retrieval with metadata filters."""
    result = retriever.retrieve_with_filters(
        query="deep learning",
        collection="test_collection",
        filters={"category": "AI"},
        top_k=5
    )

    assert result["status"] == "success"
    assert "filters" in result


def test_hybrid_search(retriever):
    """Test hybrid (dense + sparse) search."""
    result = retriever.hybrid_search(
        query="neural networks",
        collection="test_collection",
        alpha=0.7,
        top_k=5
    )

    assert result["status"] == "success"
    assert "alpha" in result
    assert result["alpha"] == 0.7


def test_multi_query_retrieve(retriever):
    """Test multi-query retrieval."""
    result = retriever.multi_query_retrieve(
        query="AI",
        collection="test_collection",
        num_queries=3,
        top_k=10
    )

    assert result["status"] == "success"
    assert "expanded_queries" in result
    assert len(result["expanded_queries"]) <= 3


def test_set_retrieval_params(retriever):
    """Test setting retrieval parameters."""
    result = retriever.set_retrieval_params(
        default_top_k=20,
        similarity_threshold=0.5
    )

    assert result["status"] == "success"
    assert result["default_top_k"] == 20
    assert result["similarity_threshold"] == 0.5


def test_similarity_computation(retriever):
    """Test similarity computation."""
    score = retriever._compute_similarity(
        "machine learning algorithms",
        "machine learning is powerful"
    )

    assert 0 <= score <= 1
    assert score > 0  # Should have some overlap


@pytest.mark.parametrize("alpha", [0.0, 0.5, 1.0])
def test_hybrid_search_alpha_values(retriever, alpha):
    """Test hybrid search with different alpha values."""
    result = retriever.hybrid_search(
        query="test",
        collection="test",
        alpha=alpha,
        top_k=5
    )

    assert result["status"] == "success"
    assert result["alpha"] == alpha


def test_empty_query(retriever):
    """Test handling of empty query."""
    result = retriever.retrieve(
        query="",
        collection="test",
        top_k=5
    )

    assert result["status"] == "success"
    # Should handle gracefully
