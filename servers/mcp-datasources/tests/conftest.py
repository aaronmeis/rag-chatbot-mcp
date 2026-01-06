"""
Shared test fixtures for mcp-datasources tests.
"""

import pytest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import DataSourcesManager


@pytest.fixture(scope="function")
def datasources():
    """Create a datasources manager for testing."""
    return DataSourcesManager()


@pytest.fixture
def temp_text_file():
    """Create a temporary text file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("This is a test document.\n")
        f.write("It contains multiple lines.\n")
        f.write("Perfect for testing file loading functionality.\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    try:
        Path(temp_path).unlink()
    except:
        pass


@pytest.fixture
def temp_markdown_file():
    """Create a temporary markdown file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write("# Test Document\n\n")
        f.write("## Introduction\n\n")
        f.write("This is a markdown file for testing.\n\n")
        f.write("## Content\n\n")
        f.write("- Item 1\n")
        f.write("- Item 2\n")
        temp_path = f.name

    yield temp_path

    try:
        Path(temp_path).unlink()
    except:
        pass


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file."""
    import json

    data = {
        "title": "Test Data",
        "items": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200}
        ],
        "metadata": {
            "version": "1.0",
            "created": "2024-01-01"
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        temp_path = f.name

    yield temp_path

    try:
        Path(temp_path).unlink()
    except:
        pass


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("name,age,city,occupation\n")
        f.write("Alice,30,NYC,Engineer\n")
        f.write("Bob,25,LA,Designer\n")
        f.write("Charlie,35,Chicago,Manager\n")
        temp_path = f.name

    yield temp_path

    try:
        Path(temp_path).unlink()
    except:
        pass


@pytest.fixture
def temp_directory():
    """Create a temporary directory with multiple files."""
    temp_dir = tempfile.mkdtemp()

    # Create various test files
    (Path(temp_dir) / "file1.txt").write_text("Content of file 1", encoding='utf-8')
    (Path(temp_dir) / "file2.txt").write_text("Content of file 2", encoding='utf-8')
    (Path(temp_dir) / "readme.md").write_text("# README\n\nProject documentation", encoding='utf-8')
    (Path(temp_dir) / "data.json").write_text('{"key": "value"}', encoding='utf-8')

    # Create subdirectory
    subdir = Path(temp_dir) / "subdir"
    subdir.mkdir()
    (subdir / "nested.txt").write_text("Nested file content", encoding='utf-8')

    yield temp_dir

    # Cleanup
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except:
        pass


@pytest.fixture
def sample_url():
    """Sample URL for testing."""
    return "https://example.com/article"


@pytest.fixture
def sample_api_endpoint():
    """Sample API endpoint."""
    return "https://api.example.com/v1/data"


@pytest.fixture
def sample_api_headers():
    """Sample API headers."""
    return {
        "Authorization": "Bearer test_token_123",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@pytest.fixture
def sample_connection_string():
    """Sample database connection string."""
    return "postgresql://testuser:testpass@localhost:5432/testdb"


@pytest.fixture
def sample_sql_query():
    """Sample SQL query."""
    return "SELECT id, content, created_at FROM documents WHERE category = 'AI' LIMIT 100"
