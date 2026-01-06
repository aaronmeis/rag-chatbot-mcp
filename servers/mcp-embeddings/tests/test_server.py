"""
Comprehensive tests for mcp-embeddings server.

Run with: pytest test_server.py -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import EmbeddingManager


class TestSingleTextEmbedding:
    """Tests for single text embedding operations."""

    def test_embed_text_basic(self, embeddings_manager, sample_text):
        """Test basic text embedding."""
        result = embeddings_manager.embed_text(text=sample_text)

        assert result["status"] == "success"
        assert "embedding" in result
        assert isinstance(result["embedding"], list)
        assert "model" in result
        assert "dimensions" in result

    def test_embed_text_dimensions(self, embeddings_manager, sample_text, expected_dimensions):
        """Test that embedding has correct dimensions."""
        model = "text-embedding-3-small"
        result = embeddings_manager.embed_text(text=sample_text, model=model)

        assert result["status"] == "success"
        assert result["dimensions"] == expected_dimensions[model]
        assert len(result["embedding"]) == expected_dimensions[model]

    def test_embed_empty_text(self, embeddings_manager):
        """Test embedding empty text."""
        result = embeddings_manager.embed_text(text="")

        assert result["status"] == "success"
        assert "embedding" in result

    def test_embed_long_text(self, embeddings_manager, sample_long_text):
        """Test embedding long text."""
        result = embeddings_manager.embed_text(text=sample_long_text)

        assert result["status"] == "success"
        assert "embedding" in result


class TestBatchEmbedding:
    """Tests for batch embedding operations."""

    def test_embed_batch_basic(self, embeddings_manager, sample_texts):
        """Test batch embedding generation."""
        result = embeddings_manager.embed_batch(texts=sample_texts)

        assert result["status"] == "success"
        assert "embeddings" in result
        assert len(result["embeddings"]) == len(sample_texts)
        assert result["count"] == len(sample_texts)

    def test_embed_batch_dimensions(self, embeddings_manager, sample_texts):
        """Test that all batch embeddings have same dimensions."""
        result = embeddings_manager.embed_batch(texts=sample_texts)

        assert result["status"] == "success"
        embeddings = result["embeddings"]

        # All embeddings should have same dimension
        first_dim = len(embeddings[0])
        assert all(len(emb) == first_dim for emb in embeddings)

    def test_embed_empty_batch(self, embeddings_manager):
        """Test embedding empty batch."""
        result = embeddings_manager.embed_batch(texts=[])

        assert result["status"] == "success"
        assert result["count"] == 0


class TestModelManagement:
    """Tests for model management operations."""

    def test_set_model_valid(self, embeddings_manager):
        """Test setting a valid model."""
        result = embeddings_manager.set_model(model="text-embedding-3-large")

        assert result["status"] == "success"
        assert result["model"] == "text-embedding-3-large"

    def test_set_model_invalid(self, embeddings_manager):
        """Test setting an invalid model."""
        result = embeddings_manager.set_model(model="nonexistent-model")

        assert result["status"] == "error"
        assert "Unknown model" in result["message"]

    def test_get_model_info(self, embeddings_manager):
        """Test getting current model information."""
        result = embeddings_manager.get_model_info()

        assert result["status"] == "success"
        assert "current_model" in result
        assert "provider" in result
        assert "dimensions" in result
        assert "available_models" in result

    def test_model_switch_affects_dimensions(self, embeddings_manager, sample_text):
        """Test that switching models changes embedding dimensions."""
        # Set to small model
        embeddings_manager.set_model(model="text-embedding-3-small")
        result1 = embeddings_manager.embed_text(text=sample_text)

        # Set to large model
        embeddings_manager.set_model(model="text-embedding-3-large")
        result2 = embeddings_manager.embed_text(text=sample_text)

        # Dimensions should be different
        assert result1["dimensions"] != result2["dimensions"]


class TestEmbeddingCaching:
    """Tests for embedding caching functionality."""

    def test_caching_identical_text(self, embeddings_manager):
        """Test that identical texts use cache."""
        text = "This is a test for caching"

        # First call
        result1 = embeddings_manager.embed_text(text=text)

        # Second call (should be cached)
        result2 = embeddings_manager.embed_text(text=text)

        assert result1["embedding"] == result2["embedding"]
        # Second call should indicate it was cached
        if "cached" in result2:
            assert result2["cached"] is True

    def test_different_text_not_cached(self, embeddings_manager):
        """Test that different texts generate new embeddings."""
        text1 = "First text"
        text2 = "Second text"

        result1 = embeddings_manager.embed_text(text=text1)
        result2 = embeddings_manager.embed_text(text=text2)

        # Embeddings should be different
        assert result1["embedding"] != result2["embedding"]


class TestModelAvailability:
    """Tests for model availability checking."""

    def test_available_models_list(self, embeddings_manager):
        """Test that available models are listed."""
        info = embeddings_manager.get_model_info()

        assert "available_models" in info
        assert isinstance(info["available_models"], list)
        assert len(info["available_models"]) > 0

    def test_openai_availability(self, embeddings_manager):
        """Test OpenAI availability flag."""
        info = embeddings_manager.get_model_info()

        assert "openai_available" in info
        assert isinstance(info["openai_available"], bool)

    def test_local_availability(self, embeddings_manager):
        """Test local model availability flag."""
        info = embeddings_manager.get_model_info()

        assert "local_available" in info
        assert isinstance(info["local_available"], bool)


class TestCustomModels:
    """Tests for custom model configuration."""

    def test_add_custom_model(self, embeddings_manager):
        """Test adding a custom model."""
        result = embeddings_manager.set_model(
            model="custom-embedding-model",
            provider="custom"
        )

        assert result["status"] == "success"
        assert result["model"] == "custom-embedding-model"
        assert "Custom model configured" in result.get("message", "")


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_embedding_workflow(self, embeddings_manager, sample_texts):
        """Test complete embedding workflow."""
        # 1. Get initial model info
        info = embeddings_manager.get_model_info()
        assert info["status"] == "success"

        # 2. Set model
        embeddings_manager.set_model(model="text-embedding-3-small")

        # 3. Embed single text
        single = embeddings_manager.embed_text(text=sample_texts[0])
        assert single["status"] == "success"

        # 4. Embed batch
        batch = embeddings_manager.embed_batch(texts=sample_texts)
        assert batch["status"] == "success"
        assert batch["count"] == len(sample_texts)

    def test_multiple_models_workflow(self, embeddings_manager, sample_text):
        """Test workflow with multiple models."""
        models = ["text-embedding-3-small", "text-embedding-3-large"]
        results = []

        for model in models:
            # Set model
            set_result = embeddings_manager.set_model(model=model)
            assert set_result["status"] == "success"

            # Generate embedding
            embed_result = embeddings_manager.embed_text(text=sample_text)
            assert embed_result["status"] == "success"
            results.append(embed_result)

        # Different models should produce different dimensions
        assert results[0]["dimensions"] != results[1]["dimensions"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
