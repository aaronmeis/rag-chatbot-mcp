"""
Shared test fixtures for mcp-vectorstore tests.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import VectorStoreManager


@pytest.fixture(scope="function")
def mock_vectorstore():
    """Create a mock vectorstore instance for testing."""
    return VectorStoreManager(backend="mock", persist_dir="./test_db")


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing deals with text and speech.",
        "Computer vision enables machines to interpret visual information.",
        "Reinforcement learning learns from rewards and penalties."
    ]


@pytest.fixture
def sample_embeddings():
    """Sample embeddings (1536 dimensions) for testing."""
    return [
        [0.1 + i * 0.01] * 1536 for i in range(5)
    ]


@pytest.fixture
def sample_metadata():
    """Sample metadata for documents."""
    return [
        {"source": "ml_guide.txt", "topic": "ML", "page": 1},
        {"source": "dl_guide.txt", "topic": "DL", "page": 1},
        {"source": "nlp_guide.txt", "topic": "NLP", "page": 2},
        {"source": "cv_guide.txt", "topic": "CV", "page": 1},
        {"source": "rl_guide.txt", "topic": "RL", "page": 3}
    ]


@pytest.fixture
def sample_ids():
    """Sample document IDs."""
    return ["doc_ml", "doc_dl", "doc_nlp", "doc_cv", "doc_rl"]


@pytest.fixture
def populated_collection(mock_vectorstore, sample_documents, sample_embeddings, sample_metadata, sample_ids):
    """A collection populated with sample data."""
    collection_name = "test_populated"

    # Create collection
    mock_vectorstore.create_collection(collection_name)

    # Add documents
    mock_vectorstore.add_documents(
        collection=collection_name,
        documents=sample_documents,
        embeddings=sample_embeddings,
        metadatas=sample_metadata,
        ids=sample_ids
    )

    return {
        "manager": mock_vectorstore,
        "collection": collection_name,
        "documents": sample_documents,
        "embeddings": sample_embeddings,
        "metadata": sample_metadata,
        "ids": sample_ids
    }


@pytest.fixture
def query_embedding():
    """Sample query embedding for search tests."""
    return [0.15] * 1536
