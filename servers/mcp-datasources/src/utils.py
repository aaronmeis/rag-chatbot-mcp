"""
Utility functions for MCP DataSources Server.
"""

import logging
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


def detect_file_type(file_path: str) -> str:
    """Detect file type from extension or MIME type.

    Args:
        file_path: Path to file

    Returns:
        File type string
    """
    ext = Path(file_path).suffix.lower()

    type_mapping = {
        '.txt': 'text',
        '.md': 'markdown',
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'doc',
        '.html': 'html',
        '.htm': 'html',
        '.json': 'json',
        '.csv': 'csv',
        '.xml': 'xml',
    }

    return type_mapping.get(ext, 'unknown')


def is_binary_file(file_path: str) -> bool:
    """Check if file is binary.

    Args:
        file_path: Path to file

    Returns:
        True if binary file
    """
    binary_extensions = {'.pdf', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx',
                        '.zip', '.tar', '.gz', '.jpg', '.png', '.gif', '.mp3', '.mp4'}

    return Path(file_path).suffix.lower() in binary_extensions


def sanitize_path(path: str, base_path: Optional[str] = None) -> str:
    """Sanitize file path to prevent directory traversal.

    Args:
        path: Input path
        base_path: Base directory to restrict to

    Returns:
        Sanitized path
    """
    path_obj = Path(path).resolve()

    if base_path:
        base_obj = Path(base_path).resolve()
        try:
            path_obj.relative_to(base_obj)
        except ValueError:
            logger.warning(f"Path {path} is outside base path {base_path}")
            raise ValueError("Invalid path: outside allowed directory")

    return str(path_obj)


def extract_text_from_html(html_content: str) -> str:
    """Extract text content from HTML.

    Args:
        html_content: HTML string

    Returns:
        Extracted text
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text
    except ImportError:
        logger.warning("beautifulsoup4 not installed, returning raw HTML")
        return html_content


def parse_connection_string(conn_str: str) -> Dict[str, str]:
    """Parse database connection string.

    Args:
        conn_str: Connection string

    Returns:
        Parsed connection components
    """
    # Simple parsing for common formats
    # Format: dialect://username:password@host:port/database
    parts = {}

    if "://" in conn_str:
        dialect, rest = conn_str.split("://", 1)
        parts["dialect"] = dialect

        if "@" in rest:
            auth, location = rest.split("@", 1)
            if ":" in auth:
                parts["username"], parts["password"] = auth.split(":", 1)
            else:
                parts["username"] = auth

            if "/" in location:
                host_port, database = location.split("/", 1)
                parts["database"] = database
            else:
                host_port = location

            if ":" in host_port:
                parts["host"], parts["port"] = host_port.split(":", 1)
            else:
                parts["host"] = host_port

    return parts


def validate_url(url: str) -> bool:
    """Validate URL format.

    Args:
        url: URL string

    Returns:
        True if valid URL
    """
    import re

    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return url_pattern.match(url) is not None


def estimate_file_read_time(file_size_bytes: int) -> float:
    """Estimate time to read file in seconds.

    Args:
        file_size_bytes: File size in bytes

    Returns:
        Estimated read time in seconds
    """
    # Assume read speed of 100 MB/s
    mb_size = file_size_bytes / (1024 * 1024)
    return mb_size / 100
