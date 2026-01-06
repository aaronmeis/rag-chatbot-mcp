"""
Shared test fixtures for mcp-embeddings tests.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import EmbeddingManager


@pytest.fixture(scope="function")
def embeddings_manager():
    """Create an embeddings manager for testing."""
    return EmbeddingManager(default_model="text-embedding-3-small")


@pytest.fixture
def sample_text():
    """Sample text for embedding."""
    return "This is a sample document about machine learning and artificial intelligence."


@pytest.fixture
def sample_texts():
    """Multiple sample texts for batch embedding."""
    return [
        "Machine learning is transforming the world.",
        "Deep learning uses neural networks.",
        "Natural language processing enables text understanding.",
        "Computer vision allows machines to see.",
        "Reinforcement learning optimizes decision making."
    ]


@pytest.fixture
def sample_long_text():
    """A longer text for testing token limits."""
    return " ".join([
        "This is a very long document that might exceed token limits.",
        "It contains multiple sentences and paragraphs.",
        "Each sentence adds to the overall token count.",
        "The system should handle this gracefully."
    ] * 50)  # Repeat to make it longer


@pytest.fixture
def expected_dimensions():
    """Expected embedding dimensions for different models."""
    return {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
        "all-MiniLM-L6-v2": 384,
        "all-mpnet-base-v2": 768,
        "e5-large-v2": 1024
    }
