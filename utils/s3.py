import hashlib
import logging
import mimetypes
import os
import uuid
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from django.conf import settings

logger = logging.getLogger(__name__)


class S3ImageUploader:
    """Utility class for uploading images to S3."""

    def __init__(self):
        # Force SigV4 (s3v4) to avoid "SigV2 authorization is not supported" errors.
        config = Config(signature_version="s3v4")
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            region_name=getattr(settings, "AWS_S3_REGION_NAME", "us-east-1"),
            endpoint_url=getattr(settings, "AWS_S3_ENDPOINT_URL", None),
            config=config,
        )
        self.bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
        self.base_url = getattr(
            settings,
            "AWS_S3_CUSTOM_DOMAIN",
            (
                f"https://{self.bucket_name}.s3.amazonaws.com"
                if self.bucket_name
                else None
            ),
        )

    def _generate_file_key(self, user_id, category, filename):
        """Generate a unique file key for S3."""
        ext = os.path.splitext(filename)[1].lower()
        unique_id = uuid.uuid4().hex[:8]
        file_hash = hashlib.md5(filename.encode(), usedforsecurity=False).hexdigest()[
            :8
        ]
        return f"users/{user_id}/{category}/{file_hash}_{unique_id}{ext}"

    def upload_file(self, file_obj, user_id, category="images", filename=None):
        """
        Upload a file to S3.

        Args:
            file_obj: File-like object or bytes
            user_id: User ID for organizing files
            category: Category subfolder (e.g., 'items', 'containers')
            filename: Original filename

        Returns:
            str: URL of the uploaded file, or None on failure
        """
        if not self.bucket_name:
            logger.error("AWS_STORAGE_BUCKET_NAME not configured")
            return None

        try:
            # Handle different file types
            if isinstance(file_obj, bytes):
                file_content = file_obj
            elif hasattr(file_obj, "read"):
                file_content = file_obj.read()
            else:
                logger.error(f"Invalid file object type: {type(file_obj)}")
                return None

            filename = filename or f"upload_{uuid.uuid4().hex[:8]}"
            file_key = self._generate_file_key(user_id, category, filename)

            # Determine content type
            content_type, _ = mimetypes.guess_type(filename)
            content_type = content_type or "application/octet-stream"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=BytesIO(file_content),
                ContentType=content_type,
            )

            # Generate URL
            url = f"{self.base_url}/{file_key}"
            logger.info(f"Successfully uploaded file to {url}")
            return url

        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
            return None

    def delete_file(self, url):
        """
        Delete a file from S3 by its URL.

        Args:
            url: The full URL of the file to delete

        Returns:
            bool: True if deletion was successful
        """
        if not self.bucket_name or not self.base_url:
            logger.error("S3 not properly configured")
            return False

        try:
            # Extract key from URL
            if url.startswith(self.base_url):
                file_key = url[len(self.base_url) + 1 :]
            else:
                logger.error(f"URL does not match expected base: {url}")
                return False

            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
            logger.info(f"Successfully deleted file: {file_key}")
            return True

        except ClientError as e:
            logger.error(f"S3 delete failed: {e}")
            return False

    def generate_presigned_upload_url(
        self, user_id, filename, content_type, category="images", expiration=300
    ):
        """
        Generate a presigned PUT URL so the client can upload directly to S3.

        Args:
            user_id: User ID for organising files under a user prefix.
            filename: Original filename (used to derive extension and key).
            content_type: MIME type of the file being uploaded.
            category: Category subfolder (default 'images').
            expiration: URL validity in seconds (default 5 minutes).

        Returns:
            dict with 'upload_url', 'file_url', and 'key', or None on failure.
        """
        if not self.bucket_name:
            logger.error("AWS_STORAGE_BUCKET_NAME not configured")
            return None

        try:
            file_key = self._generate_file_key(user_id, category, filename)

            upload_url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": file_key,
                    "ContentType": content_type,
                },
                ExpiresIn=expiration,
            )

            file_url = f"{self.base_url}/{file_key}"
            return {"upload_url": upload_url, "file_url": file_url, "key": file_key}

        except ClientError as e:
            logger.error(f"Failed to generate presigned upload URL: {e}")
            return None

    def generate_presigned_url(self, url, expiration=3600):
        """
        Generate a presigned URL for temporary access.

        Args:
            url: The full URL of the file
            expiration: Expiration time in seconds

        Returns:
            str: Presigned URL or None on failure
        """
        if not self.bucket_name or not self.base_url:
            return None

        try:
            if url.startswith(self.base_url):
                file_key = url[len(self.base_url) + 1 :]
            else:
                return None

            presigned_url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_key},
                ExpiresIn=expiration,
            )
            return presigned_url

        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None


# Singleton instance
_uploader = None


def get_s3_uploader():
    """Get or create the S3 uploader singleton."""
    global _uploader
    if _uploader is None:
        _uploader = S3ImageUploader()
    return _uploader


def upload_image_to_s3(file_obj, user_id, category="images", filename=None):
    """Convenience function to upload an image to S3."""
    uploader = get_s3_uploader()
    return uploader.upload_file(file_obj, user_id, category, filename)


def delete_image_from_s3(url):
    """Convenience function to delete an image from S3."""
    uploader = get_s3_uploader()
    return uploader.delete_file(url)
