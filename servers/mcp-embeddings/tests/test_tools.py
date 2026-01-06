"""
Tests for Embeddings tools.
"""

import pytest
from src.server import EmbeddingManager


@pytest.fixture
def embeddings():
    """Create an embeddings manager for testing."""
    return EmbeddingManager(default_model="text-embedding-3-small")


def test_embed_text(embeddings):
    """Test single text embedding."""
    result = embeddings.embed_text(
        text="This is a test document",
        model="text-embedding-3-small"
    )

    assert result["status"] == "success"
    assert "embedding" in result
    assert isinstance(result["embedding"], list)
    assert result["dimensions"] == 1536


def test_embed_batch(embeddings):
    """Test batch embedding generation."""
    texts = [
        "First document",
        "Second document",
        "Third document"
    ]

    result = embeddings.embed_batch(texts=texts)

    assert result["status"] == "success"
    assert "embeddings" in result
    assert len(result["embeddings"]) == 3
    assert result["count"] == 3


def test_set_model(embeddings):
    """Test setting embedding model."""
    result = embeddings.set_model(model="text-embedding-3-large")

    assert result["status"] == "success"
    assert result["model"] == "text-embedding-3-large"
    assert result["dimensions"] == 3072


def test_get_model_info(embeddings):
    """Test getting model information."""
    result = embeddings.get_model_info()

    assert result["status"] == "success"
    assert "current_model" in result
    assert "available_models" in result
    assert isinstance(result["available_models"], list)


def test_embedding_caching(embeddings):
    """Test that embeddings are cached."""
    text = "Test text for caching"

    # First call
    result1 = embeddings.embed_text(text)

    # Second call (should be cached)
    result2 = embeddings.embed_text(text)

    assert result1["embedding"] == result2["embedding"]
    assert result2.get("cached", False)


def test_custom_model(embeddings):
    """Test configuring custom model."""
    result = embeddings.set_model(
        model="custom-model",
        provider="custom"
    )

    assert result["status"] == "success"
    assert result["model"] == "custom-model"


@pytest.mark.parametrize("model", [
    "text-embedding-3-small",
    "text-embedding-3-large",
    "all-MiniLM-L6-v2"
])
def test_different_models(embeddings, model):
    """Test different embedding models."""
    result = embeddings.set_model(model=model)

    assert result["status"] == "success"
    assert result["model"] == model


def test_invalid_model(embeddings):
    """Test handling of invalid model."""
    result = embeddings.set_model(model="nonexistent-model")

    assert result["status"] == "error"
    assert "Unknown model" in result["message"]


def test_empty_text(embeddings):
    """Test embedding empty text."""
    result = embeddings.embed_text(text="")

    assert result["status"] == "success"
    assert "embedding" in result


def test_large_batch(embeddings):
    """Test embedding large batch of texts."""
    texts = [f"Document {i}" for i in range(50)]

    result = embeddings.embed_batch(texts=texts)

    assert result["status"] == "success"
    assert result["count"] == 50
