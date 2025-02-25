import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks, Response
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.document import DocumentStatusResponse
from app.services.firestore import get_organization_data, get_evaluation_results
from app.services.storage import get_document_download_url

logger = logging.getLogger(__name__)

router = APIRouter()

# Import document service after defining models to avoid circular imports
from app.services.ai.document_service import DocumentService
document_service = DocumentService()

class DocumentRequest(BaseModel):
    organization_id: str = Field(..., description="Organization ID")
    evaluation_id: str = Field(..., description="Evaluation ID")
    document_types: List[str] = Field(..., description="List of document types to generate")

@router.post("/generate")
async def generate_documents(request: DocumentRequest, background_tasks: BackgroundTasks):
    """
    Generate compliance documents based on evaluation results
    """
    logger.info(f"Generating documents for organization: {request.organization_id}")
    
    try:
        # Get organization data
        organization = await get_organization_data(request.organization_id)
        
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Get evaluation results
        evaluation_results = await get_evaluation_results(
            organization_id=request.organization_id,
            evaluation_id=request.evaluation_id
        )
        
        if not evaluation_results:
            raise HTTPException(status_code=404, detail="Evaluation results not found")
        
        # Create document generation record
        document_id = await document_service.create_document_generation(
            organization_id=request.organization_id,
            evaluation_id=request.evaluation_id,
            document_types=request.document_types
        )
        
        # Start document generation in background
        background_tasks.add_task(
            document_service.generate_documents,
            organization_id=request.organization_id,
            evaluation_id=request.evaluation_id,
            document_id=document_id,
            document_types=request.document_types
        )
        
        return {
            "status": "success",
            "message": "Document generation started successfully",
            "document_id": document_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating documents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate documents")

@router.get("/status/{organization_id}/{document_id}")
async def get_document_status(organization_id: str, document_id: str) -> DocumentStatusResponse:
    """
    Get the status of document generation
    """
    logger.info(f"Checking document status for organization: {organization_id}, document: {document_id}")
    
    try:
        # Get document status
        status = await document_service.get_document_status(
            organization_id=organization_id,
            document_id=document_id
        )
        
        if not status:
            raise HTTPException(status_code=404, detail="Document generation not found")
        
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking document status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to check document status")

@router.get("/download/{organization_id}/{document_id}/{document_type}")
async def download_document(organization_id: str, document_id: str, document_type: str):
    """
    Download a generated document
    """
    logger.info(f"Downloading document for organization: {organization_id}, document: {document_id}, type: {document_type}")
    
    try:
        # Get document download URL
        download_url = await get_document_download_url(
            organization_id=organization_id,
            document_id=document_id,
            document_type=document_type
        )
        
        if not download_url:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Redirect to download URL
        return Response(
            status_code=302,
            headers={"Location": download_url}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to download document")

@router.get("/list/{organization_id}")
async def list_documents(organization_id: str):
    """
    List all generated documents for an organization
    """
    logger.info(f"Listing documents for organization: {organization_id}")
    
    try:
        # Get list of documents
        documents = await document_service.list_documents(organization_id)
        
        return {
            "status": "success",
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list documents") 