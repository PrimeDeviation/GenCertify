import logging
import os
import uuid
import asyncio
from typing import List, Dict, Any, Optional
from app.services.ai.model_factory import get_ai_model
from app.services.firestore import save_document_generation, get_evaluation_results
from app.services.storage import upload_file
from app.models.document import DocumentStatus, DocumentType, DocumentFormat, DocumentStatusResponse
from fastapi import UploadFile
import io

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Service for generating compliance documents
    """
    
    def __init__(self):
        """
        Initialize document service
        """
        self.ai_model = get_ai_model()
        self.active_generations = {}  # Track active document generations
        logger.info("Document service initialized")
    
    async def create_document_generation(
        self,
        organization_id: str,
        evaluation_id: str,
        document_types: List[str]
    ) -> str:
        """
        Create a new document generation record
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            document_types: List of document types to generate
            
        Returns:
            Document generation ID
        """
        try:
            logger.info(f"Creating document generation for organization: {organization_id}")
            
            # Create document generation record
            document_id = str(uuid.uuid4())
            
            # Initialize document generation data
            document_data = {
                "id": document_id,
                "organization_id": organization_id,
                "evaluation_id": evaluation_id,
                "status": DocumentStatus.PENDING.value,
                "progress": 0.0,
                "document_types": document_types,
                "generated_documents": []
            }
            
            # Save to Firestore
            await save_document_generation(document_data)
            
            logger.info(f"Created document generation with ID: {document_id}")
            return document_id
        except Exception as e:
            logger.error(f"Error creating document generation: {str(e)}", exc_info=True)
            raise
    
    async def generate_documents(
        self,
        organization_id: str,
        evaluation_id: str,
        document_id: str,
        document_types: List[str]
    ):
        """
        Generate compliance documents
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            document_id: Document generation ID
            document_types: List of document types to generate
        """
        try:
            logger.info(f"Starting document generation for: {document_id}")
            
            # Update status to in progress
            document_data = {
                "id": document_id,
                "organization_id": organization_id,
                "evaluation_id": evaluation_id,
                "status": DocumentStatus.IN_PROGRESS.value,
                "progress": 0.0,
                "document_types": document_types,
                "generated_documents": []
            }
            
            await save_document_generation(document_data)
            
            # Track active generation
            self.active_generations[document_id] = {
                "organization_id": organization_id,
                "progress": 0.0,
                "status": DocumentStatus.IN_PROGRESS.value
            }
            
            # Get evaluation results
            evaluation = await get_evaluation_results(organization_id, evaluation_id)
            
            if not evaluation:
                raise ValueError(f"Evaluation not found: {evaluation_id}")
            
            # Process each document type
            total_documents = len(document_types)
            generated_documents = []
            
            for i, doc_type in enumerate(document_types):
                try:
                    logger.info(f"Generating document: {doc_type} for document generation: {document_id}")
                    
                    # Generate document content
                    document_content = await self.ai_model.generate_document(
                        organization_id=organization_id,
                        evaluation_id=evaluation_id,
                        document_type=doc_type,
                        evaluation_data=evaluation
                    )
                    
                    # Convert content to file-like object
                    file_content = io.BytesIO(document_content.encode("utf-8"))
                    
                    # Create file name
                    file_name = f"{doc_type.replace('_', '-')}.txt"
                    
                    # Create UploadFile object
                    upload_file_obj = UploadFile(
                        filename=file_name,
                        file=file_content,
                        content_type="text/plain"
                    )
                    
                    # Upload to Cloud Storage
                    file_url = await upload_file(upload_file_obj, organization_id)
                    
                    # Add to generated documents
                    generated_document = {
                        "document_type": doc_type,
                        "format": DocumentFormat.TXT.value,
                        "file_url": file_url,
                        "file_name": file_name,
                        "size_bytes": len(document_content),
                        "generated_at": None  # Will be set by Firestore
                    }
                    
                    generated_documents.append(generated_document)
                    
                    # Update progress
                    progress = ((i + 1) / total_documents) * 100
                    self.active_generations[document_id]["progress"] = progress
                    
                    # Update document data
                    document_data = {
                        "id": document_id,
                        "organization_id": organization_id,
                        "evaluation_id": evaluation_id,
                        "status": DocumentStatus.IN_PROGRESS.value,
                        "progress": progress,
                        "document_types": document_types,
                        "generated_documents": generated_documents
                    }
                    
                    await save_document_generation(document_data)
                    
                except Exception as e:
                    logger.error(f"Error generating document {doc_type}: {str(e)}", exc_info=True)
                    # Continue with next document type
            
            # Update status to completed
            document_data = {
                "id": document_id,
                "organization_id": organization_id,
                "evaluation_id": evaluation_id,
                "status": DocumentStatus.COMPLETED.value,
                "progress": 100.0,
                "document_types": document_types,
                "generated_documents": generated_documents,
                "completed_at": None  # Will be set by Firestore
            }
            
            await save_document_generation(document_data)
            
            # Update tracking
            self.active_generations[document_id]["status"] = DocumentStatus.COMPLETED.value
            self.active_generations[document_id]["progress"] = 100.0
            
            logger.info(f"Completed document generation: {document_id}")
            
        except Exception as e:
            logger.error(f"Error generating documents: {str(e)}", exc_info=True)
            
            # Update status to failed
            try:
                document_data = {
                    "id": document_id,
                    "organization_id": organization_id,
                    "evaluation_id": evaluation_id,
                    "status": DocumentStatus.FAILED.value,
                    "progress": self.active_generations.get(document_id, {}).get("progress", 0.0),
                    "document_types": document_types,
                    "generated_documents": []
                }
                
                await save_document_generation(document_data)
                
                if document_id in self.active_generations:
                    self.active_generations[document_id]["status"] = DocumentStatus.FAILED.value
            except Exception as inner_e:
                logger.error(f"Error updating failed document generation: {str(inner_e)}", exc_info=True)
    
    async def get_document_status(
        self,
        organization_id: str,
        document_id: str
    ) -> Optional[DocumentStatusResponse]:
        """
        Get the status of a document generation
        
        Args:
            organization_id: Organization ID
            document_id: Document generation ID
            
        Returns:
            DocumentStatus object or None if not found
        """
        try:
            logger.info(f"Getting status for document generation: {document_id}")
            
            # Check active generations first
            if document_id in self.active_generations:
                active_gen = self.active_generations[document_id]
                
                if active_gen["organization_id"] != organization_id:
                    logger.warning(f"Organization ID mismatch for document generation: {document_id}")
                    return None
                
                return DocumentStatusResponse(
                    organization_id=organization_id,
                    document_id=document_id,
                    status=active_gen["status"],
                    progress=active_gen["progress"]
                )
            
            # Otherwise, get from Firestore
            # This would be implemented to retrieve from Firestore
            
            return None
        except Exception as e:
            logger.error(f"Error getting document status: {str(e)}", exc_info=True)
            raise
    
    async def list_documents(
        self,
        organization_id: str
    ) -> List[Dict[str, Any]]:
        """
        List all generated documents for an organization
        
        Args:
            organization_id: Organization ID
            
        Returns:
            List of document generation records
        """
        try:
            logger.info(f"Listing documents for organization: {organization_id}")
            
            # This would be implemented to retrieve from Firestore
            
            return []
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}", exc_info=True)
            raise 