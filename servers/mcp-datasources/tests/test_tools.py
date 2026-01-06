"""
Tests for DataSources tools.
"""

import pytest
import tempfile
from pathlib import Path
from src.server import DataSourcesManager


@pytest.fixture
def datasources():
    """Create a datasources manager for testing."""
    return DataSourcesManager()


@pytest.fixture
def temp_text_file():
    """Create a temporary text file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test document.\nIt has multiple lines.\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def temp_directory():
    """Create a temporary directory with test files."""
    temp_dir = tempfile.mkdtemp()

    # Create test files
    (Path(temp_dir) / "file1.txt").write_text("Content of file 1")
    (Path(temp_dir) / "file2.md").write_text("# Content of file 2")
    (Path(temp_dir) / "file3.txt").write_text("Content of file 3")

    yield temp_dir

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def test_load_single_file(datasources, temp_text_file):
    """Test loading a single file."""
    result = datasources.load_files(path=temp_text_file)

    assert result["status"] == "success"
    assert result["count"] == 1
    assert len(result["documents"]) == 1
    assert result["documents"][0]["type"] == "text"


def test_load_directory(datasources, temp_directory):
    """Test loading files from a directory."""
    result = datasources.load_files(path=temp_directory, pattern="*.txt")

    assert result["status"] == "success"
    assert result["count"] == 2  # file1.txt and file3.txt


def test_load_directory_recursive(datasources, temp_directory):
    """Test recursive directory loading."""
    result = datasources.load_files(
        path=temp_directory,
        pattern="*",
        recursive=True
    )

    assert result["status"] == "success"
    assert result["count"] >= 2  # Should find .txt and .md files


def test_load_url(datasources):
    """Test URL loading (mock)."""
    result = datasources.load_url(
        url="https://example.com/article",
        extract_text=True
    )

    assert result["status"] == "success"
    assert "source_id" in result
    assert "document" in result


def test_load_api(datasources):
    """Test API endpoint loading (mock)."""
    result = datasources.load_api(
        url="https://api.example.com/data",
        method="GET",
        headers={"Authorization": "Bearer token"}
    )

    assert result["status"] == "success"
    assert result["method"] == "GET"
    assert "document" in result


def test_load_database(datasources):
    """Test database query (mock)."""
    result = datasources.load_database(
        connection_string="postgresql://user:pass@localhost/db",
        query="SELECT * FROM documents"
    )

    assert result["status"] == "success"
    assert "documents" in result
    assert result["count"] >= 0


def test_list_sources(datasources):
    """Test listing data sources."""
    # Add some sources first
    datasources.load_url("https://example.com")
    datasources.load_api("https://api.example.com")

    result = datasources.list_sources()

    assert result["status"] == "success"
    assert result["count"] >= 2
    assert isinstance(result["sources"], list)


def test_get_source_info(datasources):
    """Test getting source information."""
    # Create a source
    load_result = datasources.load_url("https://example.com")
    source_id = load_result["source_id"]

    # Get info
    result = datasources.get_source_info(source_id)

    assert result["status"] == "success"
    assert result["source_id"] == source_id
    assert result["type"] == "url"


def test_invalid_path(datasources):
    """Test handling of invalid file path."""
    result = datasources.load_files(path="/nonexistent/path")

    assert result["status"] == "error"
    assert "not found" in result["message"].lower()


def test_supported_extensions(datasources):
    """Test that supported file types are recognized."""
    extensions = [".txt", ".md", ".pdf", ".docx", ".json", ".csv"]

    for ext in extensions:
        assert ext in datasources.SUPPORTED_EXTENSIONS


def test_file_metadata(datasources, temp_text_file):
    """Test that file metadata is included."""
    result = datasources.load_files(path=temp_text_file)

    doc = result["documents"][0]
    assert "metadata" in doc
    assert "filename" in doc["metadata"]
    assert "source" in doc["metadata"]


@pytest.mark.parametrize("pattern", ["*.txt", "*.md", "*"])
def test_different_patterns(datasources, temp_directory, pattern):
    """Test different file patterns."""
    result = datasources.load_files(path=temp_directory, pattern=pattern)

    assert result["status"] == "success"
    assert result["pattern"] == pattern


def test_parse_file_error_handling(datasources):
    """Test error handling when parsing files."""
    # Try to load a non-existent file type
    with tempfile.NamedTemporaryFile(suffix='.unknown', delete=False) as f:
        f.write(b"test content")
        temp_path = f.name

    result = datasources.load_files(path=temp_path)

    # Should handle gracefully
    Path(temp_path).unlink()
