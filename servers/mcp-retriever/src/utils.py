"""
Utility functions for MCP Retriever Server.
"""

import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)


def compute_text_similarity(text1: str, text2: str) -> float:
    """Compute simple word overlap similarity between two texts.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def deduplicate_results(results: List[Dict[str, Any]], key: str = "id") -> List[Dict[str, Any]]:
    """Remove duplicate results based on a key.

    Args:
        results: List of result dictionaries
        key: Key to use for deduplication

    Returns:
        Deduplicated results
    """
    seen: Set[Any] = set()
    unique_results = []

    for result in results:
        identifier = result.get(key, id(result))
        if identifier not in seen:
            seen.add(identifier)
            unique_results.append(result)

    return unique_results


def merge_scores(scores: List[float], method: str = "max") -> float:
    """Merge multiple scores using specified method.

    Args:
        scores: List of scores
        method: Merging method ("max", "avg", "min")

    Returns:
        Merged score
    """
    if not scores:
        return 0.0

    if method == "max":
        return max(scores)
    elif method == "avg":
        return sum(scores) / len(scores)
    elif method == "min":
        return min(scores)
    else:
        return max(scores)


def normalize_scores(results: List[Dict[str, Any]], score_key: str = "score") -> List[Dict[str, Any]]:
    """Normalize scores to 0-1 range.

    Args:
        results: List of results with scores
        score_key: Key containing the score

    Returns:
        Results with normalized scores
    """
    if not results:
        return results

    scores = [r.get(score_key, 0) for r in results]
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score

    if score_range == 0:
        return results

    normalized_results = []
    for result in results:
        normalized = result.copy()
        original_score = result.get(score_key, 0)
        normalized[score_key] = (original_score - min_score) / score_range
        normalized_results.append(normalized)

    return normalized_results
