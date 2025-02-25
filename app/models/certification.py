from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class CertificationType(str, Enum):
    """
    Enum for supported certification types
    """
    ISO_27001 = "iso_27001"
    SOC_2 = "soc_2"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"

class CertificationRequirement(BaseModel):
    """
    Model representing a specific certification requirement
    """
    id: str = Field(..., description="Requirement ID")
    name: str = Field(..., description="Requirement name")
    description: str = Field(..., description="Requirement description")
    category: str = Field(..., description="Requirement category")
    certification_type: CertificationType = Field(..., description="Certification type")

class Certification(BaseModel):
    """
    Model representing a certification standard
    """
    id: Optional[str] = Field(None, description="Certification ID")
    name: str = Field(..., description="Certification name")
    description: str = Field(..., description="Certification description")
    type: CertificationType = Field(..., description="Certification type")
    requirements: List[CertificationRequirement] = Field([], description="Certification requirements")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "ISO 27001",
                "description": "Information Security Management System standard",
                "type": "iso_27001",
                "requirements": [
                    {
                        "id": "A.5.1.1",
                        "name": "Information Security Policies",
                        "description": "A set of policies for information security shall be defined, approved by management, published and communicated to employees and relevant external parties.",
                        "category": "Policies",
                        "certification_type": "iso_27001"
                    }
                ]
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary for Firestore storage
        """
        data = self.dict(exclude={"id", "created_at", "updated_at"})
        return data
    
    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]) -> "Certification":
        """
        Create model from Firestore dictionary
        """
        # Convert Firestore timestamps to datetime objects
        if "created_at" in data and data["created_at"]:
            data["created_at"] = data["created_at"].datetime
        if "updated_at" in data and data["updated_at"]:
            data["updated_at"] = data["updated_at"].datetime
            
        return cls(id=id, **data) 