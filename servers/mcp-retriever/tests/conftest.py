"""
Shared test fixtures for mcp-retriever tests.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import RetrieverManager


@pytest.fixture(scope="function")
def retriever():
    """Create a retriever instance for testing."""
    return RetrieverManager()


@pytest.fixture
def sample_query():
    """Sample query for testing."""
    return "What is machine learning and how does it work?"


@pytest.fixture
def sample_collection_name():
    """Sample collection name."""
    return "test_knowledge_base"


@pytest.fixture
def sample_search_results():
    """Mock search results for testing."""
    return [
        {
            "id": "1",
            "text": "Machine learning is a subset of AI that enables computers to learn from data.",
            "score": 0.95,
            "metadata": {"source": "ml_intro.pdf", "page": 1}
        },
        {
            "id": "2",
            "text": "Machine learning algorithms can be supervised, unsupervised, or reinforcement learning.",
            "score": 0.88,
            "metadata": {"source": "ml_types.pdf", "page": 3}
        },
        {
            "id": "3",
            "text": "Deep learning is a specialized form of machine learning using neural networks.",
            "score": 0.82,
            "metadata": {"source": "dl_overview.pdf", "page": 1}
        },
        {
            "id": "4",
            "text": "Training machine learning models requires large datasets and computational power.",
            "score": 0.75,
            "metadata": {"source": "ml_training.pdf", "page": 5}
        },
        {
            "id": "5",
            "text": "Machine learning applications include image recognition and natural language processing.",
            "score": 0.70,
            "metadata": {"source": "ml_applications.pdf", "page": 2}
        }
    ]


@pytest.fixture
def sample_filters():
    """Sample metadata filters."""
    return {
        "source": "ml_intro.pdf",
        "page": {"$gte": 1}
    }
