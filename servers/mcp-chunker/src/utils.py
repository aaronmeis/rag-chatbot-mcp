"""
Utility functions for MCP Chunker Server.
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """Clean and normalize text.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def split_by_separator(text: str, separator: str, keep_separator: bool = False) -> List[str]:
    """Split text by separator with option to keep separator.

    Args:
        text: Input text
        separator: Separator string or regex
        keep_separator: Whether to keep separator in chunks

    Returns:
        List of text chunks
    """
    if keep_separator:
        # Split but keep the separator
        parts = re.split(f'({re.escape(separator)})', text)
        chunks = []
        for i in range(0, len(parts), 2):
            chunk = parts[i]
            if i + 1 < len(parts):
                chunk += parts[i + 1]
            if chunk.strip():
                chunks.append(chunk.strip())
        return chunks
    else:
        return [p.strip() for p in text.split(separator) if p.strip()]


def calculate_overlap_indices(total_length: int, chunk_size: int, overlap: int) -> List[Tuple[int, int]]:
    """Calculate start and end indices for overlapping chunks.

    Args:
        total_length: Total length of text
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of (start, end) tuples
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap >= chunk_size:
        logger.warning(f"Overlap ({overlap}) >= chunk_size ({chunk_size}), reducing overlap")
        overlap = chunk_size // 2

    indices = []
    start = 0

    while start < total_length:
        end = min(start + chunk_size, total_length)
        indices.append((start, end))

        if end >= total_length:
            break

        start = end - overlap

    return indices


def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    """Estimate number of tokens in text.

    Args:
        text: Input text
        chars_per_token: Average characters per token

    Returns:
        Estimated token count
    """
    return int(len(text) / chars_per_token)


def find_sentence_boundaries(text: str) -> List[int]:
    """Find sentence boundary positions in text.

    Args:
        text: Input text

    Returns:
        List of character positions where sentences end
    """
    # Simple sentence boundary detection
    sentence_endings = r'[.!?]+[\s]+'
    boundaries = [0]

    for match in re.finditer(sentence_endings, text):
        boundaries.append(match.end())

    if boundaries[-1] < len(text):
        boundaries.append(len(text))

    return boundaries
