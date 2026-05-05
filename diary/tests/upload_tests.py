import pytest
from utils.s3 import S3ImageUploader


@pytest.fixture
def uploader():
    """Fixture to create a fresh S3ImageUploader instance for each test."""
    return object.__new__(S3ImageUploader)


# Test data using constants
TEST_DOMAINS = {
    "bare_domain": "example.r2.cloudflarestorage.com",
    "https_domain": "https://assets.example.com",
    "base_url": "https://example.r2.cloudflarestorage.com",
    "external_domain": "https://cdn.example.com",
    "localhost": "http://localhost:50723",
}

TEST_PATHS = {
    "file_path": "users/1/photo.jpg",
    "full_path": "users/1/photo.jpg?X-Amz-Signature=abc",
}


class TestS3BaseUrlNormalization:
    """Test URL normalization methods."""

    def test_adds_https_to_bare_domain(self, uploader):
        """Test that bare domains get https:// prefix."""
        input_domain = TEST_DOMAINS["bare_domain"]
        expected = f"https://{TEST_DOMAINS['bare_domain']}"

        result = uploader._normalize_base_url(input_domain)
        assert result == expected

    def test_keeps_existing_https_scheme(self, uploader):
        """Test that existing https:// scheme is preserved."""
        input_domain = TEST_DOMAINS["https_domain"]
        expected = TEST_DOMAINS["https_domain"].rstrip("/")

        result = uploader._normalize_base_url(input_domain)
        assert result == expected


class TestS3FileKeyExtraction:
    """Test file key extraction from URLs."""

    def test_ignores_query_string(self, uploader):
        """Test that query parameters are stripped when extracting file key."""
        uploader.base_url = TEST_DOMAINS["base_url"]
        url = f"{TEST_DOMAINS['base_url']}/{TEST_PATHS['full_path']}"

        result = uploader._extract_file_key(url)
        assert result == TEST_PATHS["file_path"]

    def test_accepts_bare_matching_domain(self, uploader):
        """Test that file key can be extracted from bare domain URLs."""
        uploader.base_url = TEST_DOMAINS["base_url"]
        url = f"{TEST_DOMAINS['bare_domain']}/{TEST_PATHS['file_path']}"

        result = uploader._extract_file_key(url)
        assert result == TEST_PATHS["file_path"]

    def test_accepts_localhost_wrapped_url(self, uploader):
        """Test that file key can be extracted from localhost-wrapped URLs."""
        uploader.base_url = TEST_DOMAINS["base_url"]
        url = f"{TEST_DOMAINS['localhost']}/{TEST_DOMAINS['bare_domain']}/{TEST_PATHS['file_path']}"

        result = uploader._extract_file_key(url)
        assert result == TEST_PATHS["file_path"]


class TestS3ManagedUrlCheck:
    """Test URL management validation."""

    def test_accepts_managed_urls(self, uploader):
        """Test that URLs with matching base domain are considered managed."""
        uploader.base_url = TEST_DOMAINS["base_url"]
        url = f"{TEST_DOMAINS['base_url']}/{TEST_PATHS['file_path']}"

        assert uploader.is_managed_url(url)

    def test_rejects_external_urls(self, uploader):
        """Test that URLs with different domains are not considered managed."""
        uploader.base_url = TEST_DOMAINS["base_url"]
        external_url = f"{TEST_DOMAINS['external_domain']}/{TEST_PATHS['file_path']}"

        assert not uploader.is_managed_url(external_url)
