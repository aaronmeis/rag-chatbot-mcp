"""
Shared test fixtures for mcp-reranker tests.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import RerankerManager


@pytest.fixture(scope="function")
def reranker():
    """Create a reranker instance for testing."""
    return RerankerManager()


@pytest.fixture
def sample_query():
    """Sample query for reranking."""
    return "How do neural networks learn?"


@pytest.fixture
def sample_documents():
    """Sample documents for reranking."""
    return [
        {
            "id": "1",
            "text": "Neural networks learn by adjusting weights through backpropagation and gradient descent.",
            "score": 0.75,
            "metadata": {"source": "nn_training.pdf", "page": 12}
        },
        {
            "id": "2",
            "text": "The learning process involves forward propagation, loss calculation, and backward propagation.",
            "score": 0.70,
            "metadata": {"source": "dl_basics.pdf", "page": 8}
        },
        {
            "id": "3",
            "text": "Machine learning algorithms can classify, predict, and cluster data effectively.",
            "score": 0.65,
            "metadata": {"source": "ml_overview.pdf", "page": 3}
        },
        {
            "id": "4",
            "text": "Deep learning uses multiple layers to progressively extract higher-level features.",
            "score": 0.60,
            "metadata": {"source": "dl_architecture.pdf", "page": 5}
        },
        {
            "id": "5",
            "text": "Training data quality significantly impacts model performance and accuracy.",
            "score": 0.55,
            "metadata": {"source": "ml_best_practices.pdf", "page": 15}
        }
    ]


@pytest.fixture
def multiple_rankings():
    """Multiple rankings for fusion testing."""
    return [
        # Ranking from dense retrieval
        [
            {"id": "1", "text": "Neural networks learn through backpropagation.", "score": 0.9},
            {"id": "2", "text": "Gradient descent optimizes neural network weights.", "score": 0.85},
            {"id": "3", "text": "Training requires labeled data and loss functions.", "score": 0.80}
        ],
        # Ranking from sparse retrieval
        [
            {"id": "2", "text": "Gradient descent optimizes neural network weights.", "score": 0.95},
            {"id": "1", "text": "Neural networks learn through backpropagation.", "score": 0.88},
            {"id": "4", "text": "Learning rate affects training convergence speed.", "score": 0.75}
        ],
        # Ranking from semantic search
        [
            {"id": "1", "text": "Neural networks learn through backpropagation.", "score": 0.92},
            {"id": "3", "text": "Training requires labeled data and loss functions.", "score": 0.86},
            {"id": "2", "text": "Gradient descent optimizes neural network weights.", "score": 0.83}
        ]
    ]


@pytest.fixture
def diverse_documents():
    """Documents with varying content for diversity testing."""
    return [
        {
            "id": "1",
            "text": "Neural networks consist of interconnected layers of neurons that process information.",
            "score": 0.9
        },
        {
            "id": "2",
            "text": "Convolutional neural networks excel at image recognition and computer vision tasks.",
            "score": 0.85
        },
        {
            "id": "3",
            "text": "Recurrent neural networks are designed for sequential data and time series analysis.",
            "score": 0.82
        },
        {
            "id": "4",
            "text": "Transformer architectures have revolutionized natural language processing applications.",
            "score": 0.80
        },
        {
            "id": "5",
            "text": "Generative adversarial networks can create realistic synthetic data and images.",
            "score": 0.78
        }
    ]
