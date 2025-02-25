import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.organization import Organization
from app.models.certification import Certification, CertificationType
from app.services.storage import upload_file
from app.services.firestore import save_organization_data, get_organization_data

logger = logging.getLogger(__name__)

router = APIRouter()

class OrganizationInput(BaseModel):
    name: str = Field(..., description="Organization name")
    industry: str = Field(..., description="Industry sector")
    size: str = Field(..., description="Organization size (e.g., Small, Medium, Large)")
    annual_revenue: Optional[str] = Field(None, description="Annual recurring revenue")
    certification_scope: str = Field(..., description="Scope of certification")
    selected_certifications: List[CertificationType] = Field(..., description="Selected certifications")

@router.post("/organization")
async def submit_organization_data(organization: OrganizationInput):
    """
    Submit organization details and selected certifications
    """
    logger.info(f"Received organization data for: {organization.name}")
    
    try:
        # Save organization data to Firestore
        org_id = await save_organization_data(organization.dict())
        
        return {
            "status": "success",
            "message": "Organization data saved successfully",
            "organization_id": org_id
        }
    except Exception as e:
        logger.error(f"Error saving organization data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save organization data")

@router.get("/certifications")
async def get_available_certifications():
    """
    Get list of available certifications
    """
    logger.info("Fetching available certifications")
    
    try:
        # Return list of available certifications
        certifications = [
            {
                "id": CertificationType.ISO_27001,
                "name": "ISO 27001",
                "description": "Information Security Management System standard"
            },
            {
                "id": CertificationType.SOC_2,
                "name": "SOC 2",
                "description": "Service Organization Control 2"
            },
            {
                "id": CertificationType.GDPR,
                "name": "GDPR",
                "description": "General Data Protection Regulation"
            },
            {
                "id": CertificationType.HIPAA,
                "name": "HIPAA",
                "description": "Health Insurance Portability and Accountability Act"
            },
            {
                "id": CertificationType.PCI_DSS,
                "name": "PCI DSS",
                "description": "Payment Card Industry Data Security Standard"
            }
        ]
        
        return {
            "status": "success",
            "certifications": certifications
        }
    except Exception as e:
        logger.error(f"Error fetching certifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch certifications")

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    organization_id: str = Form(...),
    document_type: str = Form(...),
    description: Optional[str] = Form(None)
):
    """
    Upload a document for compliance evaluation
    """
    logger.info(f"Uploading document: {file.filename} for organization: {organization_id}")
    
    try:
        # Upload file to Cloud Storage
        file_url = await upload_file(file, organization_id)
        
        # Save document metadata to Firestore
        document_data = {
            "filename": file.filename,
            "organization_id": organization_id,
            "document_type": document_type,
            "description": description,
            "file_url": file_url,
            "upload_timestamp": None  # Will be set by Firestore
        }
        
        # Save document metadata
        # Implementation in services/firestore.py
        
        return {
            "status": "success",
            "message": "Document uploaded successfully",
            "file_url": file_url
        }
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload document") 