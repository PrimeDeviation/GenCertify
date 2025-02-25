from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class DocumentType(str, Enum):
    """
    Enum for document types
    """
    INFORMATION_SECURITY_POLICY = "information_security_policy"
    SYSTEM_DESCRIPTION = "system_description"
    INCIDENT_RESPONSE_PROCEDURE = "incident_response_procedure"
    RISK_ASSESSMENT = "risk_assessment"
    DATA_PROTECTION_POLICY = "data_protection_policy"
    BUSINESS_CONTINUITY_PLAN = "business_continuity_plan"
    ACCEPTABLE_USE_POLICY = "acceptable_use_policy"
    VENDOR_MANAGEMENT_POLICY = "vendor_management_policy"

class DocumentFormat(str, Enum):
    """
    Enum for document formats
    """
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"

class DocumentStatus(str, Enum):
    """
    Enum for document generation status
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    
class DocumentStatusResponse(BaseModel):
    """
    Model for document status response
    """
    organization_id: str = Field(..., description="Organization ID")
    document_id: str = Field(..., description="Document ID")
    status: str = Field(..., description="Document generation status")
    progress: Optional[float] = Field(None, description="Generation progress (0-100)")

class GeneratedDocument(BaseModel):
    """
    Model representing a generated document
    """
    document_type: DocumentType = Field(..., description="Document type")
    format: DocumentFormat = Field(..., description="Document format")
    file_url: str = Field(..., description="Document file URL")
    file_name: str = Field(..., description="Document file name")
    size_bytes: Optional[int] = Field(None, description="Document size in bytes")
    generated_at: Optional[datetime] = Field(None, description="Generation timestamp")

class DocumentGeneration(BaseModel):
    """
    Model representing a document generation request
    """
    id: Optional[str] = Field(None, description="Document generation ID")
    organization_id: str = Field(..., description="Organization ID")
    evaluation_id: str = Field(..., description="Evaluation ID")
    status: DocumentStatus = Field(DocumentStatus.PENDING, description="Document generation status")
    progress: float = Field(0.0, description="Generation progress (0-100)")
    document_types: List[DocumentType] = Field(..., description="Document types to generate")
    generated_documents: List[GeneratedDocument] = Field([], description="Generated documents")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary for Firestore storage
        """
        data = self.dict(exclude={"id", "created_at", "updated_at", "completed_at"})
        return data
    
    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]) -> "DocumentGeneration":
        """
        Create model from Firestore dictionary
        """
        # Convert Firestore timestamps to datetime objects
        for timestamp_field in ["created_at", "updated_at", "completed_at"]:
            if timestamp_field in data and data[timestamp_field]:
                data[timestamp_field] = data[timestamp_field].datetime
                
        # Convert timestamps in generated documents
        if "generated_documents" in data:
            for doc in data["generated_documents"]:
                if "generated_at" in doc and doc["generated_at"]:
                    doc["generated_at"] = doc["generated_at"].datetime
            
        return cls(id=id, **data) 