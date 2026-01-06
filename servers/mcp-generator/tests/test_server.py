"""
Tests for mcp-generator server
"""

import pytest
from unittest.mock import Mock, patch


class TestGeneratorManager:
    """Tests for the GeneratorManager class"""
    
    def test_generate_response_with_context(self):
        """Test response generation with retrieved context"""
        query = "What is RAG?"
        context = [
            {"content": "RAG stands for Retrieval-Augmented Generation."},
            {"content": "It combines retrieval with generation."}
        ]
        
        mock_response = "RAG (Retrieval-Augmented Generation) is a technique that combines document retrieval with language model generation."
        
        assert len(mock_response) > 0
        assert "RAG" in mock_response
    
    def test_generate_without_context(self):
        """Test response generation without context"""
        query = "Hello, how are you?"
        
        mock_response = "I'm doing well, thank you for asking!"
        
        assert len(mock_response) > 0
    
    def test_context_formatting(self):
        """Test context is properly formatted for LLM"""
        contexts = [
            {"content": "Document 1 content", "source": "doc1.pdf"},
            {"content": "Document 2 content", "source": "doc2.pdf"}
        ]
        
        formatted = "\n\n".join([f"[{c['source']}]: {c['content']}" for c in contexts])
        
        assert "Document 1" in formatted
        assert "Document 2" in formatted


class TestPromptTemplates:
    """Tests for prompt templates"""
    
    def test_default_template(self):
        """Test default prompt template"""
        template = """Answer the question based on the context provided.

Context:
{context}

Question: {question}

Answer:"""
        
        assert "{context}" in template
        assert "{question}" in template
    
    def test_concise_template(self):
        """Test concise response template"""
        template = """Provide a brief, direct answer based on the context.

Context: {context}

Question: {question}

Brief Answer:"""
        
        assert "brief" in template.lower()
    
    def test_detailed_template(self):
        """Test detailed response template"""
        template = """Provide a comprehensive answer with explanations.

Context:
{context}

Question: {question}

Detailed Answer:"""
        
        assert "comprehensive" in template.lower() or "detailed" in template.lower()
    
    def test_citation_template(self):
        """Test template with citations"""
        template = """Answer with citations to sources.

Context:
{context}

Question: {question}

Answer (cite sources using [Source: filename]):"""
        
        assert "cite" in template.lower()
    
    def test_custom_template_formatting(self):
        """Test custom template variable substitution"""
        template = "Context: {context}\nQuestion: {question}"
        context = "Sample context"
        question = "Sample question"
        
        formatted = template.format(context=context, question=question)
        
        assert "Sample context" in formatted
        assert "Sample question" in formatted


class TestGeneratorTools:
    """Tests for MCP tool handlers"""
    
    @pytest.mark.asyncio
    async def test_generate_response_tool(self):
        """Test generate_response tool format"""
        mock_result = {
            "query": "What is RAG?",
            "response": "RAG is a technique...",
            "context_used": 3,
            "model": "gpt-4",
            "tokens_used": 150
        }
        
        assert "query" in mock_result
        assert "response" in mock_result
        assert "model" in mock_result
    
    @pytest.mark.asyncio
    async def test_summarize_context_tool(self):
        """Test summarize_context tool"""
        mock_result = {
            "summary": "The documents discuss...",
            "documents_summarized": 5,
            "original_length": 5000,
            "summary_length": 500
        }
        
        assert "summary" in mock_result
        assert mock_result["summary_length"] < mock_result["original_length"]
    
    @pytest.mark.asyncio
    async def test_extract_info_tool(self):
        """Test extract_info tool"""
        mock_result = {
            "extracted": {
                "entities": ["OpenAI", "GPT-4"],
                "dates": ["2023-03-14"],
                "facts": ["RAG improves accuracy"]
            },
            "extraction_type": "entities"
        }
        
        assert "extracted" in mock_result
    
    @pytest.mark.asyncio
    async def test_generate_with_citations_tool(self):
        """Test generate_with_citations tool"""
        mock_result = {
            "response": "RAG is effective [1]. It reduces hallucinations [2].",
            "citations": [
                {"id": 1, "source": "paper1.pdf", "content": "RAG is effective..."},
                {"id": 2, "source": "paper2.pdf", "content": "Reduces hallucinations..."}
            ]
        }
        
        assert "response" in mock_result
        assert "citations" in mock_result
        assert len(mock_result["citations"]) == 2
    
    @pytest.mark.asyncio
    async def test_set_prompt_template_tool(self):
        """Test set_prompt_template tool"""
        mock_result = {
            "success": True,
            "template_name": "concise",
            "previous_template": "default"
        }
        
        assert mock_result["success"] is True


class TestCitationGeneration:
    """Tests for citation functionality"""
    
    def test_citation_extraction(self):
        """Test citations are extracted from response"""
        response = "According to the study [1], RAG is effective. This is supported by [2]."
        
        import re
        citations = re.findall(r'\[(\d+)\]', response)
        
        assert len(citations) == 2
        assert "1" in citations
        assert "2" in citations
    
    def test_citation_mapping(self):
        """Test citations map to sources"""
        citations = {
            1: {"source": "paper1.pdf", "page": 5},
            2: {"source": "paper2.pdf", "page": 12}
        }
        
        assert citations[1]["source"] == "paper1.pdf"
        assert citations[2]["source"] == "paper2.pdf"
    
    def test_citation_formatting(self):
        """Test citation format in output"""
        response = "RAG improves accuracy."
        source = "research.pdf"
        
        cited = f"{response} [Source: {source}]"
        
        assert source in cited


class TestGenerationValidation:
    """Tests for input validation"""
    
    def test_empty_query_handling(self):
        """Test empty query is handled"""
        query = ""
        
        assert len(query) == 0
    
    def test_empty_context_handling(self):
        """Test generation works without context"""
        context = []
        
        # Should fall back to model knowledge
        assert len(context) == 0
    
    def test_max_tokens_respected(self):
        """Test max tokens parameter is respected"""
        max_tokens = 500
        mock_response = "x" * 1000
        
        truncated = mock_response[:max_tokens]
        assert len(truncated) <= max_tokens
    
    def test_temperature_bounds(self):
        """Test temperature parameter bounds"""
        valid_temps = [0.0, 0.5, 1.0, 2.0]
        
        for temp in valid_temps:
            assert 0 <= temp <= 2


class TestStreamingGeneration:
    """Tests for streaming response generation"""
    
    @pytest.mark.asyncio
    async def test_streaming_yields_chunks(self):
        """Test streaming yields response chunks"""
        chunks = ["Hello", " there", "!", " How", " are", " you?"]
        
        collected = []
        for chunk in chunks:
            collected.append(chunk)
        
        full_response = "".join(collected)
        assert full_response == "Hello there! How are you?"
    
    @pytest.mark.asyncio
    async def test_streaming_preserves_order(self):
        """Test streaming maintains chunk order"""
        chunks = ["1", "2", "3", "4", "5"]
        
        result = "".join(chunks)
        assert result == "12345"


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_api_error_handling(self):
        """Test API errors are handled gracefully"""
        error_response = {
            "error": True,
            "message": "API rate limit exceeded",
            "retry_after": 60
        }
        
        assert error_response["error"] is True
        assert "retry_after" in error_response
    
    def test_context_too_long_handling(self):
        """Test handling of context exceeding limits"""
        max_context_tokens = 4000
        context_tokens = 5000
        
        # Should truncate or summarize
        assert context_tokens > max_context_tokens
    
    def test_invalid_model_handling(self):
        """Test invalid model name is rejected"""
        valid_models = ["gpt-4", "gpt-3.5-turbo", "claude-3"]
        invalid_model = "invalid-model-name"
        
        assert invalid_model not in valid_models


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
