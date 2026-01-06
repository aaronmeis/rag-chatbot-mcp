"""
Shared test fixtures for mcp-generator tests.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import GeneratorManager


@pytest.fixture(scope="function")
def generator():
    """Create a generator instance for testing."""
    return GeneratorManager()


@pytest.fixture
def sample_query():
    """Sample query for generation."""
    return "What is machine learning and how does it work?"


@pytest.fixture
def sample_context():
    """Sample context documents for generation."""
    return [
        {
            "text": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns and make predictions.",
            "metadata": {"source": "ml_intro.pdf", "page": 1, "author": "Dr. Smith"}
        },
        {
            "text": "Machine learning algorithms can be categorized into supervised learning, unsupervised learning, and reinforcement learning. Each type has different use cases and requirements.",
            "metadata": {"source": "ml_types.pdf", "page": 3, "author": "Prof. Johnson"}
        },
        {
            "text": "The machine learning workflow typically involves data collection, preprocessing, model training, evaluation, and deployment. Each step is crucial for building effective models.",
            "metadata": {"source": "ml_workflow.pdf", "page": 5, "author": "Dr. Lee"}
        }
    ]


@pytest.fixture
def large_context():
    """Larger context for testing limits."""
    documents = []
    for i in range(20):
        documents.append({
            "text": f"Document {i + 1}: This is a sample document containing information about various aspects of machine learning, artificial intelligence, and data science. " * 10,
            "metadata": {"source": f"doc_{i+1}.pdf", "page": i + 1}
        })
    return documents


@pytest.fixture
def sample_schema():
    """Sample extraction schema."""
    return {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Main topic of the document"
            },
            "key_points": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of key points"
            },
            "authors": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of authors mentioned"
            },
            "complexity_level": {
                "type": "string",
                "enum": ["beginner", "intermediate", "advanced"],
                "description": "Complexity level of the content"
            },
            "confidence_score": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Confidence in the extraction"
            }
        },
        "required": ["topic", "key_points"]
    }


@pytest.fixture
def custom_template():
    """Custom prompt template for testing."""
    return """Based on the following sources, provide a detailed answer.

Sources:
{context}

Question: {query}

Please provide a comprehensive answer with specific references to the sources."""
