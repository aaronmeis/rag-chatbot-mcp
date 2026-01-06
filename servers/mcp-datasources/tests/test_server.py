"""
Comprehensive tests for mcp-datasources server.

Run with: pytest test_server.py -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import DataSourcesManager


class TestFileLoading:
    """Tests for file loading operations."""

    def test_load_single_text_file(self, datasources, temp_text_file):
        """Test loading a single text file."""
        result = datasources.load_files(path=temp_text_file)

        assert result["status"] == "success"
        assert result["count"] == 1
        assert len(result["documents"]) == 1
        assert result["documents"][0]["type"] == "text"
        assert "test document" in result["documents"][0]["content"].lower()

    def test_load_markdown_file(self, datasources, temp_markdown_file):
        """Test loading markdown files."""
        result = datasources.load_files(path=temp_markdown_file)

        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["documents"][0]["type"] == "markdown"
        assert "# Test Document" in result["documents"][0]["content"]

    def test_load_json_file(self, datasources, temp_json_file):
        """Test loading JSON files."""
        result = datasources.load_files(path=temp_json_file)

        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["documents"][0]["type"] == "json"
        assert "Test Data" in result["documents"][0]["content"]

    def test_load_csv_file(self, datasources, temp_csv_file):
        """Test loading CSV files."""
        result = datasources.load_files(path=temp_csv_file)

        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["documents"][0]["type"] == "csv"
        assert "Alice" in result["documents"][0]["content"]


class TestDirectoryLoading:
    """Tests for directory loading operations."""

    def test_load_directory_non_recursive(self, datasources, temp_directory):
        """Test loading files from directory (non-recursive)."""
        result = datasources.load_files(path=temp_directory, pattern="*.txt", recursive=False)

        assert result["status"] == "success"
        assert result["count"] >= 2  # file1.txt and file2.txt
        assert result["recursive"] is False

    def test_load_directory_recursive(self, datasources, temp_directory):
        """Test recursive directory loading."""
        result = datasources.load_files(path=temp_directory, pattern="*.txt", recursive=True)

        assert result["status"] == "success"
        assert result["count"] >= 3  # Including nested.txt
        assert result["recursive"] is True

    def test_load_all_files(self, datasources, temp_directory):
        """Test loading all file types."""
        result = datasources.load_files(path=temp_directory, pattern="*", recursive=True)

        assert result["status"] == "success"
        assert result["count"] >= 4  # Multiple file types


class TestURLLoading:
    """Tests for URL loading operations."""

    def test_load_url(self, datasources, sample_url):
        """Test URL loading (mock)."""
        result = datasources.load_url(url=sample_url, extract_text=True)

        assert result["status"] == "success"
        assert "source_id" in result
        assert result["url"] == sample_url
        assert "document" in result

    def test_list_sources_includes_url(self, datasources, sample_url):
        """Test that loaded URL appears in sources list."""
        # Load a URL
        load_result = datasources.load_url(url=sample_url)
        source_id = load_result["source_id"]

        # List sources
        list_result = datasources.list_sources()

        assert list_result["status"] == "success"
        assert any(s["id"] == source_id for s in list_result["sources"])


class TestAPILoading:
    """Tests for API loading operations."""

    def test_load_api_get(self, datasources, sample_api_endpoint):
        """Test API GET request (mock)."""
        result = datasources.load_api(url=sample_api_endpoint, method="GET")

        assert result["status"] == "success"
        assert result["method"] == "GET"
        assert "document" in result

    def test_load_api_with_headers(self, datasources, sample_api_endpoint, sample_api_headers):
        """Test API with authentication headers."""
        result = datasources.load_api(
            url=sample_api_endpoint,
            method="GET",
            headers=sample_api_headers
        )

        assert result["status"] == "success"
        assert result["method"] == "GET"


class TestDatabaseLoading:
    """Tests for database loading operations."""

    def test_load_database(self, datasources, sample_connection_string, sample_sql_query):
        """Test database query (mock)."""
        result = datasources.load_database(
            connection_string=sample_connection_string,
            query=sample_sql_query
        )

        assert result["status"] == "success"
        assert "documents" in result
        assert result["count"] >= 0


class TestSourceManagement:
    """Tests for source management operations."""

    def test_list_sources_empty(self, datasources):
        """Test listing sources when none exist."""
        result = datasources.list_sources()

        assert result["status"] == "success"
        assert "sources" in result
        assert isinstance(result["sources"], list)

    def test_list_sources_populated(self, datasources, temp_text_file, sample_url):
        """Test listing sources after loading some."""
        # Load file
        datasources.load_files(path=temp_text_file)

        # Load URL
        datasources.load_url(url=sample_url)

        # List sources
        result = datasources.list_sources()

        assert result["status"] == "success"
        assert result["count"] >= 2

    def test_get_source_info(self, datasources, temp_text_file):
        """Test getting source information."""
        # Load file
        load_result = datasources.load_files(path=temp_text_file)
        source_id = load_result["source_id"]

        # Get info
        result = datasources.get_source_info(source_id=source_id)

        assert result["status"] == "success"
        assert result["source_id"] == source_id
        assert result["type"] == "files"

    def test_get_nonexistent_source(self, datasources):
        """Test getting info for non-existent source."""
        result = datasources.get_source_info(source_id="nonexistent_source")

        assert result["status"] == "error"
        assert "not found" in result["message"].lower()


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_file_path(self, datasources):
        """Test handling of invalid file path."""
        result = datasources.load_files(path="/nonexistent/path/file.txt")

        assert result["status"] == "error"
        assert "not found" in result["message"].lower()

    def test_file_metadata(self, datasources, temp_text_file):
        """Test that file metadata is properly extracted."""
        result = datasources.load_files(path=temp_text_file)

        doc = result["documents"][0]
        assert "metadata" in doc
        assert "filename" in doc["metadata"]
        assert "source" in doc["metadata"]


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_workflow(self, datasources, temp_directory):
        """Test complete workflow: load -> list -> get info."""
        # Load directory
        load_result = datasources.load_files(path=temp_directory, pattern="*", recursive=True)
        source_id = load_result["source_id"]

        assert load_result["status"] == "success"
        assert load_result["count"] > 0

        # List sources
        list_result = datasources.list_sources()
        assert any(s["id"] == source_id for s in list_result["sources"])

        # Get source info
        info_result = datasources.get_source_info(source_id=source_id)
        assert info_result["status"] == "success"
        assert info_result["type"] == "files"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
