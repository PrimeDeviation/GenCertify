from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Organization(BaseModel):
    """
    Organization model representing a company or entity seeking certification
    """
    id: Optional[str] = Field(None, description="Organization ID")
    name: str = Field(..., description="Organization name")
    industry: str = Field(..., description="Industry sector")
    size: str = Field(..., description="Organization size (e.g., Small, Medium, Large)")
    annual_revenue: Optional[str] = Field(None, description="Annual recurring revenue")
    certification_scope: str = Field(..., description="Scope of certification")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Acme Corp",
                "industry": "Technology",
                "size": "Medium",
                "annual_revenue": "$5M-$10M",
                "certification_scope": "Cloud-based SaaS product and internal operations"
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary for Firestore storage
        """
        data = self.dict(exclude={"id", "created_at", "updated_at"})
        return data
    
    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]) -> "Organization":
        """
        Create model from Firestore dictionary
        """
        # Convert Firestore timestamps to datetime objects
        if "created_at" in data and data["created_at"]:
            data["created_at"] = data["created_at"].datetime
        if "updated_at" in data and data["updated_at"]:
            data["updated_at"] = data["updated_at"].datetime
            
        return cls(id=id, **data) 