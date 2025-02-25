from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from app.models.certification import CertificationType

class EvaluationStatus(str, Enum):
    """
    Enum for evaluation status
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    
class EvaluationStatusResponse(BaseModel):
    """
    Model for evaluation status response
    """
    organization_id: str = Field(..., description="Organization ID")
    evaluation_id: str = Field(..., description="Evaluation ID")
    status: str = Field(..., description="Evaluation status")
    progress: Optional[float] = Field(None, description="Evaluation progress (0-100)")

class RequirementEvaluation(BaseModel):
    """
    Model representing the evaluation of a specific certification requirement
    """
    requirement_id: str = Field(..., description="Requirement ID")
    name: str = Field(..., description="Requirement name")
    description: str = Field(..., description="Requirement description")
    category: str = Field(..., description="Requirement category")
    certification_type: CertificationType = Field(..., description="Certification type")
    compliance_score: float = Field(..., description="Compliance score (0-100)")
    findings: List[str] = Field([], description="Evaluation findings")
    recommendations: List[str] = Field([], description="Recommendations for improvement")

class CertificationEvaluation(BaseModel):
    """
    Model representing the evaluation of a certification standard
    """
    certification_type: CertificationType = Field(..., description="Certification type")
    overall_score: float = Field(..., description="Overall compliance score (0-100)")
    requirement_evaluations: List[RequirementEvaluation] = Field([], description="Requirement evaluations")
    summary: str = Field(..., description="Evaluation summary")
    strengths: List[str] = Field([], description="Identified strengths")
    weaknesses: List[str] = Field([], description="Identified weaknesses")
    recommendations: List[str] = Field([], description="Overall recommendations")

class Evaluation(BaseModel):
    """
    Model representing a certification readiness evaluation
    """
    id: Optional[str] = Field(None, description="Evaluation ID")
    organization_id: str = Field(..., description="Organization ID")
    status: EvaluationStatus = Field(EvaluationStatus.PENDING, description="Evaluation status")
    progress: float = Field(0.0, description="Evaluation progress (0-100)")
    certification_types: List[CertificationType] = Field(..., description="Certification types being evaluated")
    certification_evaluations: List[CertificationEvaluation] = Field([], description="Certification evaluations")
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
    def from_dict(cls, id: str, data: Dict[str, Any]) -> "Evaluation":
        """
        Create model from Firestore dictionary
        """
        # Convert Firestore timestamps to datetime objects
        for timestamp_field in ["created_at", "updated_at", "completed_at"]:
            if timestamp_field in data and data[timestamp_field]:
                data[timestamp_field] = data[timestamp_field].datetime
            
        return cls(id=id, **data) 