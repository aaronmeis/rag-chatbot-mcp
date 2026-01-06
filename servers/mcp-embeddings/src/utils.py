"""
Utility functions for MCP Embeddings Server.
"""

import hashlib
import logging
from typing import List, Any

logger = logging.getLogger(__name__)


def hash_text(text: str) -> str:
    """Generate a stable hash for text (for caching).

    Args:
        text: Input text

    Returns:
        Hash string
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def truncate_text(text: str, max_tokens: int = 8191, encoding: str = "cl100k_base") -> str:
    """Truncate text to fit within token limit.

    Args:
        text: Input text
        max_tokens: Maximum number of tokens
        encoding: Tokenizer encoding to use

    Returns:
        Truncated text
    """
    # Simple character-based truncation (rough approximation: 1 token ≈ 4 chars)
    max_chars = max_tokens * 4

    if len(text) <= max_chars:
        return text

    logger.warning(f"Text truncated from {len(text)} to {max_chars} characters")
    return text[:max_chars]


def batch_texts(texts: List[str], max_batch_size: int = 100) -> List[List[str]]:
    """Split texts into batches for efficient processing.

    Args:
        texts: List of texts
        max_batch_size: Maximum batch size

    Returns:
        List of text batches
    """
    batches = []
    for i in range(0, len(texts), max_batch_size):
        batches.append(texts[i:i + max_batch_size])
    return batches


def estimate_cost(num_tokens: int, model: str = "text-embedding-3-small") -> float:
    """Estimate API cost for embedding generation.

    Args:
        num_tokens: Number of tokens
        model: Model name

    Returns:
        Estimated cost in USD
    """
    # Pricing as of 2024 (per 1M tokens)
    pricing = {
        "text-embedding-3-small": 0.02,
        "text-embedding-3-large": 0.13,
        "text-embedding-ada-002": 0.10,
    }

    price_per_million = pricing.get(model, 0.02)
    return (num_tokens / 1_000_000) * price_per_million


def validate_embedding(embedding: List[float], expected_dim: int) -> bool:
    """Validate embedding vector.

    Args:
        embedding: Embedding vector
        expected_dim: Expected dimension

    Returns:
        True if valid
    """
    if not isinstance(embedding, list):
        return False

    if len(embedding) != expected_dim:
        logger.error(f"Invalid embedding dimension: {len(embedding)}, expected {expected_dim}")
        return False

    if not all(isinstance(x, (int, float)) for x in embedding):
        logger.error("Embedding contains non-numeric values")
        return False

    return True
