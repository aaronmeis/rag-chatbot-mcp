"""
Shared test fixtures for mcp-chunker tests.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import ChunkerManager


@pytest.fixture(scope="function")
def chunker():
    """Create a chunker instance for testing."""
    return ChunkerManager(default_chunk_size=512, default_overlap=50)


@pytest.fixture
def sample_short_text():
    """Short sample text for chunking."""
    return "This is a short text. It has a few sentences. Perfect for testing."


@pytest.fixture
def sample_long_text():
    """Longer sample text for chunking."""
    return """
    Machine Learning: A Comprehensive Overview

    Machine learning is a subset of artificial intelligence that focuses on developing
    systems that can learn from and make decisions based on data. Unlike traditional
    programming where rules are explicitly coded, machine learning algorithms build
    models based on sample data.

    There are three main types of machine learning: supervised learning, unsupervised
    learning, and reinforcement learning. Supervised learning uses labeled data to train
    models, unsupervised learning finds patterns in unlabeled data, and reinforcement
    learning learns through trial and error with rewards and penalties.

    Applications of machine learning are widespread and growing. They include image
    recognition, natural language processing, recommendation systems, fraud detection,
    and autonomous vehicles. The field continues to evolve rapidly with new techniques
    and applications emerging regularly.

    Deep learning, a subset of machine learning, uses neural networks with multiple
    layers to process data. This approach has been particularly successful in areas
    like computer vision and natural language processing, achieving human-level or
    even superhuman performance on certain tasks.

    The future of machine learning looks promising, with ongoing research into areas
    like few-shot learning, transfer learning, and explainable AI. As computational
    power increases and more data becomes available, machine learning systems will
    likely become even more powerful and ubiquitous.
    """


@pytest.fixture
def sample_document_with_metadata():
    """Sample document with metadata for testing."""
    return {
        "text": """
        Chapter 1: Introduction to Neural Networks

        Neural networks are computing systems inspired by biological neural networks.
        They consist of interconnected nodes or neurons that process information.

        Each neuron receives inputs, processes them, and produces an output. The connections
        between neurons have weights that are adjusted during training.

        Chapter 2: Training Neural Networks

        Training involves adjusting weights to minimize error on training data. This is
        typically done using backpropagation and gradient descent algorithms.
        """,
        "metadata": {
            "title": "Neural Networks Guide",
            "author": "Dr. Jane Smith",
            "source": "nn_guide.pdf",
            "date": "2024-01-15",
            "pages": 45
        }
    }


@pytest.fixture
def sample_paragraphs():
    """Text with clear paragraph boundaries."""
    return """First paragraph with some content here.
This is still the first paragraph.

Second paragraph starts here.
It has multiple lines too.

Third paragraph is the last one.
It concludes the document."""
