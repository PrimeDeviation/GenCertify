import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.evaluation import EvaluationStatusResponse
from app.services.firestore import get_organization_data, save_evaluation_result

logger = logging.getLogger(__name__)

router = APIRouter()

# Import and initialize evaluation service after defining models to avoid circular imports
from app.services.ai.evaluation_service import EvaluationService
evaluation_service = EvaluationService()

class EvaluationRequest(BaseModel):
    organization_id: str = Field(..., description="Organization ID")
    certification_types: List[str] = Field(..., description="List of certification types to evaluate")

@router.post("/start")
async def start_evaluation(request: EvaluationRequest, background_tasks: BackgroundTasks):
    """
    Start a certification readiness evaluation
    """
    logger.info(f"Starting evaluation for organization: {request.organization_id}")
    
    try:
        # Get organization data
        organization = await get_organization_data(request.organization_id)
        
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Create evaluation record
        evaluation_id = await evaluation_service.create_evaluation(
            organization_id=request.organization_id,
            certification_types=request.certification_types
        )
        
        # Start evaluation in background
        background_tasks.add_task(
            evaluation_service.run_evaluation,
            organization_id=request.organization_id,
            evaluation_id=evaluation_id,
            certification_types=request.certification_types
        )
        
        return {
            "status": "success",
            "message": "Evaluation started successfully",
            "evaluation_id": evaluation_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting evaluation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to start evaluation")

@router.get("/status/{organization_id}/{evaluation_id}")
async def get_evaluation_status(organization_id: str, evaluation_id: str) -> EvaluationStatusResponse:
    """
    Get the status of an ongoing evaluation
    """
    logger.info(f"Checking evaluation status for organization: {organization_id}, evaluation: {evaluation_id}")
    
    try:
        # Get evaluation status
        status = await evaluation_service.get_evaluation_status(
            organization_id=organization_id,
            evaluation_id=evaluation_id
        )
        
        if not status:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking evaluation status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to check evaluation status")

@router.get("/results/{organization_id}/{evaluation_id}")
async def get_evaluation_results(organization_id: str, evaluation_id: str):
    """
    Get the results of a completed evaluation
    """
    logger.info(f"Fetching evaluation results for organization: {organization_id}, evaluation: {evaluation_id}")
    
    try:
        # Get evaluation results
        results = await evaluation_service.get_evaluation_results(
            organization_id=organization_id,
            evaluation_id=evaluation_id
        )
        
        if not results:
            raise HTTPException(status_code=404, detail="Evaluation results not found")
        
        return {
            "status": "success",
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching evaluation results: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch evaluation results") 