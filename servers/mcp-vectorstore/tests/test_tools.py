"""
Tests for VectorStore tools.
"""

import pytest
from src.tools import VectorStoreTools


@pytest.fixture
def vectorstore():
    """Create a mock vectorstore instance for testing."""
    return VectorStoreTools(backend="mock", persist_dir="./test_db")


def test_create_collection(vectorstore):
    """Test creating a vector collection."""
    result = vectorstore.create_collection("test_collection", metadata={"description": "test"})

    assert result["status"] == "success"
    assert result["collection"] == "test_collection"


def test_add_documents(vectorstore):
    """Test adding documents to a collection."""
    # First create collection
    vectorstore.create_collection("test_collection")

    # Add documents
    documents = ["Doc 1", "Doc 2", "Doc 3"]
    embeddings = [[0.1] * 1536, [0.2] * 1536, [0.3] * 1536]
    ids = ["doc1", "doc2", "doc3"]

    result = vectorstore.add_documents(
        collection="test_collection",
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    assert result["status"] == "success"
    assert result["added"] == 3


def test_search_similar(vectorstore):
    """Test searching for similar documents."""
    # Setup
    vectorstore.create_collection("test_collection")
    documents = ["Machine learning is great", "AI is the future"]
    embeddings = [[0.1] * 1536, [0.2] * 1536]
    vectorstore.add_documents("test_collection", documents, embeddings)

    # Search
    query_embedding = [0.15] * 1536
    result = vectorstore.search_similar("test_collection", query_embedding, top_k=2)

    assert result["status"] == "success"
    assert isinstance(result["results"], list)


def test_delete_documents(vectorstore):
    """Test deleting documents from a collection."""
    # Setup
    vectorstore.create_collection("test_collection")
    documents = ["Doc 1", "Doc 2"]
    embeddings = [[0.1] * 1536, [0.2] * 1536]
    ids = ["doc1", "doc2"]
    vectorstore.add_documents("test_collection", documents, embeddings, ids=ids)

    # Delete
    result = vectorstore.delete_documents("test_collection", ["doc1"])

    assert result["status"] == "success"
    assert result["deleted"] == 1


def test_list_collections(vectorstore):
    """Test listing all collections."""
    vectorstore.create_collection("col1")
    vectorstore.create_collection("col2")

    result = vectorstore.list_collections()

    assert result["status"] == "success"
    assert "col1" in result["collections"]
    assert "col2" in result["collections"]


def test_get_collection_stats(vectorstore):
    """Test getting collection statistics."""
    vectorstore.create_collection("test_collection")
    documents = ["Doc 1", "Doc 2", "Doc 3"]
    embeddings = [[0.1] * 1536, [0.2] * 1536, [0.3] * 1536]
    vectorstore.add_documents("test_collection", documents, embeddings)

    result = vectorstore.get_collection_stats("test_collection")

    assert result["status"] == "success"
    assert result["collection"] == "test_collection"
    assert result["count"] == 3


def test_invalid_collection(vectorstore):
    """Test operations on non-existent collection."""
    result = vectorstore.get_collection_stats("nonexistent")

    assert result["status"] == "error"
    assert "not found" in result["message"].lower()


@pytest.mark.parametrize("backend", ["mock", "chromadb", "faiss"])
def test_different_backends(backend):
    """Test vectorstore with different backends."""
    vs = VectorStoreTools(backend=backend)
    result = vs.create_collection("test")

    assert result["status"] == "success"
