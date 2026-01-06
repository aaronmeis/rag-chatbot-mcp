"""
Tests for Chunker tools.
"""

import pytest
from src.server import ChunkerManager


@pytest.fixture
def chunker():
    """Create a chunker instance for testing."""
    return ChunkerManager(default_chunk_size=512, default_overlap=50)


def test_chunk_text_fixed(chunker):
    """Test fixed-size chunking."""
    text = "This is a test document. " * 100

    result = chunker.chunk_text(text, strategy="fixed", chunk_size=200, overlap=20)

    assert result["status"] == "success"
    assert result["strategy"] == "fixed"
    assert result["total_chunks"] > 0
    assert all(c["char_count"] <= 200 for c in result["chunks"])


def test_chunk_text_recursive(chunker):
    """Test recursive chunking."""
    text = """
    This is paragraph one.
    It has multiple sentences.

    This is paragraph two.
    Also with multiple sentences.
    """

    result = chunker.chunk_text(text, strategy="recursive", chunk_size=100)

    assert result["status"] == "success"
    assert result["strategy"] == "recursive"
    assert result["total_chunks"] > 0


def test_chunk_text_sentence(chunker):
    """Test sentence-based chunking."""
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."

    result = chunker.chunk_text(text, strategy="sentence", chunk_size=50)

    assert result["status"] == "success"
    assert result["strategy"] == "sentence"


def test_chunk_text_paragraph(chunker):
    """Test paragraph-based chunking."""
    text = """
    First paragraph here.

    Second paragraph here.

    Third paragraph here.
    """

    result = chunker.chunk_text(text, strategy="paragraph")

    assert result["status"] == "success"
    assert result["strategy"] == "paragraph"
    assert result["total_chunks"] == 3


def test_chunk_document(chunker):
    """Test chunking document with metadata."""
    document = {
        "text": "This is a test document. " * 50,
        "metadata": {
            "source": "test.txt",
            "author": "Test Author"
        }
    }

    result = chunker.chunk_document(document, strategy="recursive")

    assert result["status"] == "success"
    assert all("metadata" in chunk for chunk in result["chunks"])
    assert all(chunk["metadata"]["source"] == "test.txt" for chunk in result["chunks"])


def test_set_chunk_size(chunker):
    """Test setting default chunk size."""
    result = chunker.set_chunk_size(1024)

    assert result["status"] == "success"
    assert result["chunk_size"] == 1024
    assert chunker.chunk_size == 1024


def test_set_overlap(chunker):
    """Test setting chunk overlap."""
    result = chunker.set_overlap(100)

    assert result["status"] == "success"
    assert result["overlap"] == 100
    assert chunker.overlap == 100


def test_preview_chunks(chunker):
    """Test chunk preview."""
    text = "This is a test. " * 20

    result = chunker.preview_chunks(text, strategy="sentence")

    assert result["status"] == "success"
    assert result["preview"] is True
    assert "summary" in result
    assert "total_chunks" in result["summary"]


def test_empty_text(chunker):
    """Test chunking empty text."""
    result = chunker.chunk_text("", strategy="recursive")

    assert result["status"] == "success"
    assert result["total_chunks"] == 0


@pytest.mark.parametrize("strategy", ["fixed", "recursive", "sentence", "paragraph"])
def test_all_strategies(chunker, strategy):
    """Test all chunking strategies."""
    text = "This is a test document. " * 10

    result = chunker.chunk_text(text, strategy=strategy)

    assert result["status"] == "success"
    assert result["strategy"] == strategy


def test_chunk_overlap(chunker):
    """Test that overlap is preserved between chunks."""
    text = "abcdefghijklmnopqrstuvwxyz" * 10

    result = chunker.chunk_text(text, strategy="fixed", chunk_size=50, overlap=10)

    # Chunks should overlap
    assert result["total_chunks"] > 1
    # First chunk should have some overlap with second
