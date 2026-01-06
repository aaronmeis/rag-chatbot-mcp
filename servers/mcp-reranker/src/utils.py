"""
Utility functions for MCP Reranker Server.
"""

import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)


def normalize_scores(scores: List[float]) -> List[float]:
    """Normalize scores to 0-1 range.

    Args:
        scores: List of scores

    Returns:
        Normalized scores
    """
    if not scores:
        return scores

    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score

    if score_range == 0:
        return [0.5] * len(scores)

    return [(s - min_score) / score_range for s in scores]


def compute_reciprocal_rank_score(rank: int, k: int = 60) -> float:
    """Compute reciprocal rank fusion score.

    Args:
        rank: Document rank (0-indexed)
        k: Constant for RRF formula

    Returns:
        RRF score
    """
    return 1.0 / (k + rank + 1)


def calculate_diversity_score(doc_text: str, selected_texts: List[str]) -> float:
    """Calculate diversity score relative to already selected documents.

    Args:
        doc_text: Candidate document text
        selected_texts: Texts of already selected documents

    Returns:
        Diversity score (lower = more diverse)
    """
    if not selected_texts:
        return 0.0

    doc_words = set(doc_text.lower().split())

    max_similarity = 0.0
    for sel_text in selected_texts:
        sel_words = set(sel_text.lower().split())
        if doc_words and sel_words:
            similarity = len(doc_words & sel_words) / len(doc_words | sel_words)
            max_similarity = max(max_similarity, similarity)

    return max_similarity


def merge_rankings(rankings: List[List[Dict[str, Any]]], method: str = "rrf", k: int = 60) -> List[Dict[str, Any]]:
    """Merge multiple rankings into a single ranking.

    Args:
        rankings: List of ranked result lists
        method: Merging method ("rrf", "average", "max")
        k: RRF constant

    Returns:
        Merged ranking
    """
    doc_scores = {}

    for ranking in rankings:
        for rank, doc in enumerate(ranking):
            doc_id = doc.get("id", str(hash(doc.get("text", ""))))

            if method == "rrf":
                score = compute_reciprocal_rank_score(rank, k)
            elif method == "average":
                score = doc.get("score", 1.0 / (rank + 1))
            elif method == "max":
                score = doc.get("score", 1.0)
            else:
                score = compute_reciprocal_rank_score(rank, k)

            if doc_id not in doc_scores:
                doc_scores[doc_id] = {"doc": doc, "score": 0, "count": 0}

            doc_scores[doc_id]["score"] += score
            doc_scores[doc_id]["count"] += 1

    # Convert to list and sort
    merged = []
    for doc_id, data in doc_scores.items():
        result = data["doc"].copy()
        result["merged_score"] = data["score"]
        result["appearance_count"] = data["count"]
        merged.append(result)

    merged.sort(key=lambda x: x["merged_score"], reverse=True)
    return merged


def apply_mmr_selection(documents: List[Dict[str, Any]], lambda_param: float = 0.5, top_k: int = 10) -> List[Dict[str, Any]]:
    """Apply Maximal Marginal Relevance for diversity.

    Args:
        documents: Candidate documents with scores
        lambda_param: Trade-off between relevance and diversity (0-1)
        top_k: Number of documents to select

    Returns:
        Selected documents
    """
    if not documents or top_k <= 0:
        return []

    selected = [documents[0]]
    remaining = documents[1:]

    while len(selected) < top_k and remaining:
        best_score = -float('inf')
        best_idx = 0

        for idx, doc in enumerate(remaining):
            relevance = doc.get("score", doc.get("rerank_score", 0.5))
            doc_text = doc.get("text", "")

            diversity = 1.0 - calculate_diversity_score(doc_text, [d.get("text", "") for d in selected])

            mmr_score = lambda_param * relevance + (1 - lambda_param) * diversity

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        selected.append(remaining.pop(best_idx))

    return selected
