"""
Tests for mcp-vectorstore server

Run with: pytest test_server.py -v
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import VectorStoreManager


class TestVectorStoreManager:
    """Test suite for VectorStoreManager class."""
    
    @pytest.fixture
    def manager(self):
        """Create a mock vector store manager for testing."""
        return VectorStoreManager(backend="mock", persist_dir="./test_db")
    
    def test_create_collection(self, manager):
        """Test collection creation."""
        result = manager.create_collection(
            name="test_collection",
            metadata={"description": "Test collection"}
        )
        
        assert result["status"] == "success"
        assert result["collection"] == "test_collection"
    
    def test_create_collection_with_dimension(self, manager):
        """Test collection creation with custom embedding dimension."""
        result = manager.create_collection(
            name="test_collection_768",
            embedding_dimension=768
        )
        
        assert result["status"] == "success"
    
    def test_add_documents(self, manager):
        """Test adding documents to a collection."""
        # First create collection
        manager.create_collection(name="test_docs")
        
        # Add documents
        result = manager.add_documents(
            collection="test_docs",
            documents=["Document 1", "Document 2", "Document 3"],
            embeddings=[[0.1] * 1536, [0.2] * 1536, [0.3] * 1536],
            metadatas=[
                {"source": "file1.txt"},
                {"source": "file2.txt"},
                {"source": "file3.txt"}
            ]
        )
        
        assert result["status"] == "success"
        assert result["added"] == 3
    
    def test_add_documents_with_ids(self, manager):
        """Test adding documents with custom IDs."""
        manager.create_collection(name="test_ids")
        
        result = manager.add_documents(
            collection="test_ids",
            documents=["Doc A", "Doc B"],
            embeddings=[[0.1] * 1536, [0.2] * 1536],
            ids=["custom_id_1", "custom_id_2"]
        )
        
        assert result["status"] == "success"
        assert result["added"] == 2
    
    def test_search_similar(self, manager):
        """Test similarity search."""
        # Setup
        manager.create_collection(name="search_test")
        manager.add_documents(
            collection="search_test",
            documents=["Hello world", "Goodbye world", "Hello there"],
            embeddings=[[0.1] * 1536, [0.2] * 1536, [0.15] * 1536]
        )
        
        # Search
        result = manager.search_similar(
            collection="search_test",
            query_embedding=[0.1] * 1536,
            top_k=2
        )
        
        assert result["status"] == "success"
        assert "results" in result
        assert len(result["results"]) <= 2
    
    def test_search_with_filter(self, manager):
        """Test similarity search with metadata filter."""
        manager.create_collection(name="filter_test")
        manager.add_documents(
            collection="filter_test",
            documents=["Doc 1", "Doc 2"],
            embeddings=[[0.1] * 1536, [0.2] * 1536],
            metadatas=[{"category": "A"}, {"category": "B"}]
        )
        
        result = manager.search_similar(
            collection="filter_test",
            query_embedding=[0.15] * 1536,
            top_k=5,
            filter={"category": "A"}
        )
        
        assert result["status"] == "success"
    
    def test_delete_documents(self, manager):
        """Test document deletion."""
        manager.create_collection(name="delete_test")
        manager.add_documents(
            collection="delete_test",
            documents=["To delete", "To keep"],
            embeddings=[[0.1] * 1536, [0.2] * 1536],
            ids=["del_1", "keep_1"]
        )
        
        result = manager.delete_documents(
            collection="delete_test",
            ids=["del_1"]
        )
        
        assert result["status"] == "success"
        assert result["deleted"] == 1
    
    def test_list_collections(self, manager):
        """Test listing collections."""
        # Create some collections
        manager.create_collection(name="coll_1")
        manager.create_collection(name="coll_2")
        
        result = manager.list_collections()
        
        assert result["status"] == "success"
        assert "collections" in result
        assert "coll_1" in result["collections"]
        assert "coll_2" in result["collections"]
    
    def test_get_collection_stats(self, manager):
        """Test getting collection statistics."""
        manager.create_collection(name="stats_test")
        manager.add_documents(
            collection="stats_test",
            documents=["Doc 1", "Doc 2", "Doc 3"],
            embeddings=[[0.1] * 1536, [0.2] * 1536, [0.3] * 1536]
        )
        
        result = manager.get_collection_stats(collection="stats_test")
        
        assert result["status"] == "success"
        assert result["collection"] == "stats_test"
        assert result["count"] == 3
    
    def test_nonexistent_collection(self, manager):
        """Test operations on non-existent collection."""
        result = manager.get_collection_stats(collection="nonexistent")
        
        assert result["status"] == "error" or "not found" in str(result).lower()


class TestVectorStoreIntegration:
    """Integration tests for complete workflows."""
    
    @pytest.fixture
    def manager(self):
        return VectorStoreManager(backend="mock", persist_dir="./test_integration")
    
    def test_full_workflow(self, manager):
        """Test complete workflow: create -> add -> search -> delete."""
        # Create collection
        create_result = manager.create_collection(name="workflow_test")
        assert create_result["status"] == "success"
        
        # Add documents
        add_result = manager.add_documents(
            collection="workflow_test",
            documents=[
                "Machine learning is a subset of artificial intelligence.",
                "Deep learning uses neural networks with many layers.",
                "Natural language processing deals with text and speech."
            ],
            embeddings=[
                [0.1] * 1536,
                [0.2] * 1536,
                [0.3] * 1536
            ],
            metadatas=[
                {"topic": "ML"},
                {"topic": "DL"},
                {"topic": "NLP"}
            ],
            ids=["doc_ml", "doc_dl", "doc_nlp"]
        )
        assert add_result["status"] == "success"
        assert add_result["added"] == 3
        
        # Check stats
        stats = manager.get_collection_stats(collection="workflow_test")
        assert stats["count"] == 3
        
        # Search
        search_result = manager.search_similar(
            collection="workflow_test",
            query_embedding=[0.15] * 1536,
            top_k=2
        )
        assert search_result["status"] == "success"
        assert len(search_result["results"]) <= 2
        
        # Delete one document
        delete_result = manager.delete_documents(
            collection="workflow_test",
            ids=["doc_ml"]
        )
        assert delete_result["status"] == "success"
        
        # Verify deletion
        stats_after = manager.get_collection_stats(collection="workflow_test")
        assert stats_after["count"] == 2
    
    def test_batch_operations(self, manager):
        """Test batch add and search operations."""
        manager.create_collection(name="batch_test")
        
        # Batch add - 100 documents
        documents = [f"Document number {i}" for i in range(100)]
        embeddings = [[i * 0.01] * 1536 for i in range(100)]
        
        result = manager.add_documents(
            collection="batch_test",
            documents=documents,
            embeddings=embeddings
        )
        
        assert result["status"] == "success"
        assert result["added"] == 100
        
        # Search should work on large collection
        search_result = manager.search_similar(
            collection="batch_test",
            query_embedding=[0.5] * 1536,
            top_k=10
        )
        
        assert search_result["status"] == "success"
        assert len(search_result["results"]) <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
