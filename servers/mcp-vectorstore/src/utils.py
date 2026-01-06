"""
Utility functions for MCP VectorStore Server.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def validate_embedding_dimension(embeddings: List[List[float]], expected_dim: int) -> bool:
    """Validate that all embeddings have the expected dimension.

    Args:
        embeddings: List of embedding vectors
        expected_dim: Expected dimension

    Returns:
        True if all embeddings match expected dimension
    """
    if not embeddings:
        return True

    for i, emb in enumerate(embeddings):
        if len(emb) != expected_dim:
            logger.warning(f"Embedding {i} has dimension {len(emb)}, expected {expected_dim}")
            return False
    return True


def normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize metadata to ensure compatibility with vector stores.

    Args:
        metadata: Raw metadata dictionary

    Returns:
        Normalized metadata
    """
    normalized = {}
    for key, value in metadata.items():
        # Convert non-serializable types
        if isinstance(value, (list, tuple)):
            normalized[key] = str(value)
        elif isinstance(value, dict):
            normalized[key] = str(value)
        else:
            normalized[key] = value
    return normalized


def calculate_distance_to_similarity(distance: float, metric: str = "l2") -> float:
    """Convert distance metric to similarity score.

    Args:
        distance: Distance value
        metric: Distance metric type ("l2", "cosine", "ip")

    Returns:
        Similarity score between 0 and 1
    """
    if metric == "l2":
        # L2 distance to similarity
        return 1.0 / (1.0 + distance)
    elif metric == "cosine":
        # Cosine distance to similarity
        return 1.0 - distance
    elif metric == "ip":
        # Inner product (already similarity-like)
        return distance
    else:
        return 1.0 / (1.0 + distance)


def batch_documents(documents: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """Split documents into batches for processing.

    Args:
        documents: List of documents
        batch_size: Maximum batch size

    Returns:
        List of document batches
    """
    batches = []
    for i in range(0, len(documents), batch_size):
        batches.append(documents[i:i + batch_size])
    return batches
