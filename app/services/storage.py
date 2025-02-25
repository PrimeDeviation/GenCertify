import logging
import os
import uuid
from typing import Optional
from fastapi import UploadFile
from google.cloud import storage
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Initialize Storage client with error handling for development
try:
    storage_client = storage.Client()
    logger.info("Connected to Cloud Storage successfully")

    # Get bucket name from environment variable
    BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME", "gencertify-bucket")

    # Ensure bucket exists
    def ensure_bucket_exists():
        """
        Ensure the storage bucket exists, create it if it doesn't
        """
        try:
            bucket = storage_client.bucket(BUCKET_NAME)
            if not bucket.exists():
                logger.info(f"Creating bucket: {BUCKET_NAME}")
                bucket = storage_client.create_bucket(BUCKET_NAME)
            return bucket
        except Exception as e:
            logger.error(f"Error ensuring bucket exists: {str(e)}", exc_info=True)
            raise

    # Get or create bucket
    bucket = ensure_bucket_exists()
    
except Exception as e:
    logger.warning(f"Failed to connect to Cloud Storage: {e}")
    logger.warning("Running in development mode with mock Storage")
    storage_client = None
    bucket = None

async def upload_file(file: UploadFile, organization_id: str) -> str:
    """
    Upload a file to Cloud Storage
    
    Args:
        file: File to upload
        organization_id: Organization ID
        
    Returns:
        File URL
    """
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{organization_id}/{str(uuid.uuid4())}{file_extension}"
        
        if bucket is None:
            # Mock implementation for development
            # Just read the file to ensure it's valid but don't store it
            await file.read()
            mock_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{unique_filename}"
            logger.info(f"[MOCK] Uploaded file: {file.filename} to {unique_filename}")
            return mock_url
            
        # Create blob
        blob = bucket.blob(unique_filename)
        
        # Upload file
        contents = await file.read()
        blob.upload_from_string(
            contents,
            content_type=file.content_type
        )
        
        # Get public URL
        file_url = blob.public_url
        
        logger.info(f"Uploaded file: {file.filename} to {unique_filename}")
        return file_url
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        raise

async def get_document_download_url(organization_id: str, document_id: str, document_type: str) -> Optional[str]:
    """
    Get a signed URL for downloading a document
    
    Args:
        organization_id: Organization ID
        document_id: Document ID
        document_type: Document type
        
    Returns:
        Signed URL for downloading the document or None if not found
    """
    try:
        # Construct blob path
        blob_path = f"{organization_id}/{document_id}/{document_type}"
        
        if bucket is None:
            # Mock implementation for development
            mock_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_path}?mock=true"
            logger.info(f"[MOCK] Generated download URL for document: {blob_path}")
            return mock_url
            
        # Check if blob exists
        blob = bucket.blob(blob_path)
        if not blob.exists():
            logger.warning(f"Document not found: {blob_path}")
            return None
        
        # Generate signed URL (valid for 1 hour)
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=1),
            method="GET"
        )
        
        logger.info(f"Generated download URL for document: {blob_path}")
        return signed_url
    except Exception as e:
        logger.error(f"Error generating document download URL: {str(e)}", exc_info=True)
        raise

async def delete_file(file_path: str) -> bool:
    """
    Delete a file from Cloud Storage
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if bucket is None:
            # Mock implementation for development
            logger.info(f"[MOCK] Deleted file: {file_path}")
            return True
            
        # Delete blob
        blob = bucket.blob(file_path)
        if not blob.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        blob.delete()
        
        logger.info(f"Deleted file: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}", exc_info=True)
        raise 