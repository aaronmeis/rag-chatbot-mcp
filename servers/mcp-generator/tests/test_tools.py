"""
Tests for Generator tools.
"""

import pytest
from src.server import GeneratorManager


@pytest.fixture
def generator():
    """Create a generator instance for testing."""
    return GeneratorManager()


@pytest.fixture
def sample_context():
    """Sample context documents."""
    return [
        {
            "text": "Machine learning is a subset of artificial intelligence.",
            "metadata": {"source": "ml_intro.pdf"}
        },
        {
            "text": "Neural networks are inspired by biological neurons.",
            "metadata": {"source": "nn_guide.md"}
        },
        {
            "text": "Deep learning uses multiple layers of neural networks.",
            "metadata": {"source": "dl_book.txt"}
        }
    ]


def test_generate_response(generator, sample_context):
    """Test basic response generation."""
    result = generator.generate_response(
        query="What is machine learning?",
        context=sample_context,
        template="default"
    )

    assert result["status"] == "success"
    assert "response" in result
    assert result["context_docs"] == 3


def test_summarize_context(generator, sample_context):
    """Test context summarization."""
    result = generator.summarize_context(
        documents=sample_context,
        max_length=500
    )

    assert result["status"] == "success"
    assert "summary" in result
    assert result["documents_summarized"] == 3


def test_extract_info(generator, sample_context):
    """Test structured information extraction."""
    schema = {
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "key_concepts": {"type": "array"},
            "confidence": {"type": "number"}
        }
    }

    result = generator.extract_info(
        documents=sample_context,
        schema=schema
    )

    assert result["status"] == "success"
    assert "extracted" in result
    assert "topic" in result["extracted"]


def test_generate_with_citations(generator, sample_context):
    """Test generation with citations."""
    result = generator.generate_with_citations(
        query="How do neural networks work?",
        context=sample_context
    )

    assert result["status"] == "success"
    assert "citations" in result
    assert len(result["citations"]) > 0


def test_set_prompt_template(generator):
    """Test setting custom prompt template."""
    custom_template = "Context: {context}\n\nQ: {query}\n\nA:"

    result = generator.set_prompt_template(
        name="custom",
        template=custom_template
    )

    assert result["status"] == "success"
    assert result["template_name"] == "custom"
    assert "custom" in result["available_templates"]


def test_format_context(generator, sample_context):
    """Test context formatting."""
    formatted = generator._format_context(sample_context)

    assert isinstance(formatted, str)
    assert "[1]" in formatted
    assert "[2]" in formatted
    assert "ml_intro.pdf" in formatted


def test_empty_context(generator):
    """Test generation with empty context."""
    result = generator.generate_response(
        query="Test question",
        context=[],
        template="default"
    )

    assert result["status"] == "success"
    assert result["context_docs"] == 0


@pytest.mark.parametrize("template", ["default", "concise", "detailed", "citation"])
def test_all_templates(generator, sample_context, template):
    """Test all built-in templates."""
    result = generator.generate_response(
        query="What is AI?",
        context=sample_context,
        template=template
    )

    assert result["status"] == "success"
    assert result["template"] == template


def test_long_context(generator):
    """Test with many context documents."""
    long_context = [
        {"text": f"Document {i} content", "metadata": {"source": f"doc{i}.txt"}}
        for i in range(20)
    ]

    result = generator.generate_response(
        query="Test",
        context=long_context
    )

    assert result["status"] == "success"
    assert result["context_docs"] == 20


def test_citation_format(generator, sample_context):
    """Test that citations are properly formatted."""
    result = generator.generate_with_citations(
        query="Test",
        context=sample_context
    )

    citations = result["citations"]
    assert all("index" in c for c in citations)
    assert all("source" in c for c in citations)
    assert all("text_snippet" in c for c in citations)
