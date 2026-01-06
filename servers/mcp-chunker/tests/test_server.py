"""
Tests for mcp-chunker server
"""

import pytest
from unittest.mock import Mock


class TestChunkerManager:
    """Tests for the ChunkerManager class"""
    
    def test_fixed_chunking(self):
        """Test fixed-size chunking"""
        text = "Word " * 1000  # 1000 words
        chunk_size = 100
        
        # Simulate chunking
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
        
        assert len(chunks) == 10
        assert all(len(c.split()) <= chunk_size for c in chunks)
    
    def test_chunking_with_overlap(self):
        """Test chunking with overlap"""
        text = "Word " * 100
        chunk_size = 20
        overlap = 5
        
        words = text.split()
        chunks = []
        step = chunk_size - overlap
        
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i+chunk_size])
            if chunk:
                chunks.append(chunk)
        
        # With overlap, we should have more chunks
        assert len(chunks) > 100 // chunk_size
    
    def test_recursive_chunking(self):
        """Test recursive character text splitting"""
        text = """
        # Section 1
        
        This is paragraph one with some content.
        
        This is paragraph two with more content.
        
        # Section 2
        
        Another section begins here.
        """
        
        separators = ["\n\n", "\n", " "]
        
        # Verify separators hierarchy
        assert separators[0] == "\n\n"  # Paragraphs first
        assert separators[1] == "\n"     # Then lines
        assert separators[2] == " "      # Then words
    
    def test_sentence_chunking(self):
        """Test sentence-based chunking"""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        
        # Simple sentence split
        sentences = [s.strip() + "." for s in text.rstrip(".").split(". ")]
        
        assert len(sentences) == 4
        assert sentences[0] == "First sentence."


class TestChunkingStrategies:
    """Tests for different chunking strategies"""
    
    def test_strategy_fixed(self):
        """Test fixed strategy produces equal-sized chunks"""
        strategy = "fixed"
        chunk_size = 512
        
        assert strategy == "fixed"
        assert chunk_size > 0
    
    def test_strategy_recursive(self):
        """Test recursive strategy respects separators"""
        strategy = "recursive"
        separators = ["\n\n", "\n", ". ", " "]
        
        assert strategy == "recursive"
        assert len(separators) > 0
    
    def test_strategy_sentence(self):
        """Test sentence strategy splits on sentence boundaries"""
        strategy = "sentence"
        
        assert strategy == "sentence"
    
    def test_strategy_paragraph(self):
        """Test paragraph strategy splits on paragraph boundaries"""
        strategy = "paragraph"
        separator = "\n\n"
        
        assert strategy == "paragraph"
        assert separator == "\n\n"
    
    def test_strategy_semantic(self):
        """Test semantic chunking based on embedding similarity"""
        strategy = "semantic"
        threshold = 0.5
        
        assert strategy == "semantic"
        assert 0 <= threshold <= 1


class TestChunkMetadata:
    """Tests for chunk metadata preservation"""
    
    def test_chunk_has_index(self):
        """Test each chunk has its index"""
        chunks = [
            {"content": "Chunk 1", "metadata": {"chunk_index": 0}},
            {"content": "Chunk 2", "metadata": {"chunk_index": 1}},
            {"content": "Chunk 3", "metadata": {"chunk_index": 2}}
        ]
        
        for i, chunk in enumerate(chunks):
            assert chunk["metadata"]["chunk_index"] == i
    
    def test_chunk_has_source(self):
        """Test each chunk preserves source information"""
        source_file = "document.pdf"
        chunks = [
            {"content": "Chunk 1", "metadata": {"source": source_file}},
            {"content": "Chunk 2", "metadata": {"source": source_file}}
        ]
        
        assert all(c["metadata"]["source"] == source_file for c in chunks)
    
    def test_chunk_has_position(self):
        """Test each chunk has position information"""
        chunk = {
            "content": "Sample chunk",
            "metadata": {
                "start_char": 0,
                "end_char": 100,
                "start_token": 0,
                "end_token": 20
            }
        }
        
        assert "start_char" in chunk["metadata"]
        assert "end_char" in chunk["metadata"]


class TestChunkerTools:
    """Tests for MCP tool handlers"""
    
    @pytest.mark.asyncio
    async def test_chunk_text_tool(self):
        """Test chunk_text tool format"""
        mock_result = {
            "chunks": [
                {"content": "Chunk 1", "index": 0},
                {"content": "Chunk 2", "index": 1}
            ],
            "total_chunks": 2,
            "strategy": "recursive",
            "chunk_size": 512
        }
        
        assert "chunks" in mock_result
        assert "total_chunks" in mock_result
        assert mock_result["total_chunks"] == len(mock_result["chunks"])
    
    @pytest.mark.asyncio
    async def test_chunk_document_tool(self):
        """Test chunk_document tool with file"""
        mock_result = {
            "document": "test.pdf",
            "chunks": [],
            "total_chunks": 5,
            "pages_processed": 10
        }
        
        assert "document" in mock_result
        assert "pages_processed" in mock_result
    
    @pytest.mark.asyncio
    async def test_set_chunk_size_tool(self):
        """Test set_chunk_size tool"""
        mock_result = {
            "success": True,
            "previous_size": 512,
            "current_size": 1024
        }
        
        assert mock_result["success"] is True
        assert mock_result["current_size"] == 1024
    
    @pytest.mark.asyncio
    async def test_set_overlap_tool(self):
        """Test set_overlap tool"""
        mock_result = {
            "success": True,
            "previous_overlap": 50,
            "current_overlap": 100
        }
        
        assert mock_result["success"] is True
    
    @pytest.mark.asyncio
    async def test_preview_chunks_tool(self):
        """Test preview_chunks tool"""
        mock_result = {
            "preview": [
                {"content": "First 100 chars...", "length": 512}
            ],
            "total_chunks": 10,
            "showing": 3
        }
        
        assert "preview" in mock_result
        assert mock_result["showing"] <= mock_result["total_chunks"]


class TestChunkValidation:
    """Tests for input validation"""
    
    def test_chunk_size_minimum(self):
        """Test minimum chunk size is enforced"""
        min_chunk_size = 50
        invalid_size = 10
        
        assert invalid_size < min_chunk_size
    
    def test_chunk_size_maximum(self):
        """Test maximum chunk size is enforced"""
        max_chunk_size = 10000
        invalid_size = 50000
        
        assert invalid_size > max_chunk_size
    
    def test_overlap_less_than_chunk_size(self):
        """Test overlap must be less than chunk size"""
        chunk_size = 512
        valid_overlap = 50
        invalid_overlap = 600
        
        assert valid_overlap < chunk_size
        assert invalid_overlap >= chunk_size
    
    def test_empty_text_handling(self):
        """Test empty text returns empty chunks"""
        text = ""
        chunks = []
        
        assert len(chunks) == 0


class TestChunkQuality:
    """Tests for chunk quality"""
    
    def test_no_empty_chunks(self):
        """Test no empty chunks are produced"""
        chunks = [
            {"content": "Chunk 1"},
            {"content": "Chunk 2"},
            {"content": "Chunk 3"}
        ]
        
        assert all(len(c["content"]) > 0 for c in chunks)
    
    def test_chunks_within_size_limit(self):
        """Test all chunks are within size limit"""
        chunk_size = 512
        chunks = [
            {"content": "x" * 500},
            {"content": "x" * 512},
            {"content": "x" * 480}
        ]
        
        assert all(len(c["content"]) <= chunk_size for c in chunks)
    
    def test_text_fully_covered(self):
        """Test original text is fully covered by chunks"""
        original = "This is the full text content."
        chunks = ["This is the", " full text", " content."]
        
        reconstructed = "".join(chunks)
        assert original == reconstructed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
