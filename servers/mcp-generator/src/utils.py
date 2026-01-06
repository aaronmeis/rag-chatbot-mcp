"""
Utility functions for MCP Generator Server.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def format_context_with_citations(documents: List[Dict[str, Any]]) -> str:
    """Format documents into context string with citation markers.

    Args:
        documents: List of document dictionaries

    Returns:
        Formatted context string
    """
    formatted = []
    for i, doc in enumerate(documents, 1):
        text = doc.get("text", doc.get("content", ""))
        source = doc.get("metadata", {}).get("source", f"Document {i}")
        formatted.append(f"[{i}] {source}:\n{text}")

    return "\n\n".join(formatted)


def extract_citations(response_text: str) -> List[int]:
    """Extract citation numbers from response text.

    Args:
        response_text: Generated response with [1], [2] style citations

    Returns:
        List of cited document numbers
    """
    import re
    citations = re.findall(r'\[(\d+)\]', response_text)
    return sorted(set(int(c) for c in citations))


def truncate_context(documents: List[Dict[str, Any]], max_length: int = 4000) -> List[Dict[str, Any]]:
    """Truncate context documents to fit within length limit.

    Args:
        documents: List of documents
        max_length: Maximum total character length

    Returns:
        Truncated document list
    """
    truncated = []
    current_length = 0

    for doc in documents:
        text = doc.get("text", "")
        if current_length + len(text) > max_length:
            # Add partial document
            remaining = max_length - current_length
            if remaining > 100:  # Only add if meaningful amount left
                truncated_doc = doc.copy()
                truncated_doc["text"] = text[:remaining] + "..."
                truncated.append(truncated_doc)
            break

        truncated.append(doc)
        current_length += len(text)

    return truncated


def validate_template(template: str) -> bool:
    """Validate prompt template has required placeholders.

    Args:
        template: Template string

    Returns:
        True if valid
    """
    required_placeholders = ["{context}", "{query}"]

    for placeholder in required_placeholders:
        if placeholder not in template:
            logger.error(f"Template missing required placeholder: {placeholder}")
            return False

    return True


def estimate_prompt_tokens(prompt: str, chars_per_token: float = 4.0) -> int:
    """Estimate number of tokens in prompt.

    Args:
        prompt: Prompt string
        chars_per_token: Average characters per token

    Returns:
        Estimated token count
    """
    return int(len(prompt) / chars_per_token)


def create_summary_from_docs(documents: List[Dict[str, Any]], max_sentences: int = 5) -> str:
    """Create a quick summary from documents.

    Args:
        documents: List of documents
        max_sentences: Maximum number of sentences to include

    Returns:
        Summary text
    """
    import re

    all_text = " ".join(doc.get("text", "") for doc in documents)
    sentences = re.split(r'[.!?]+', all_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Take first max_sentences
    summary_sentences = sentences[:max_sentences]
    return ". ".join(summary_sentences) + "." if summary_sentences else ""
