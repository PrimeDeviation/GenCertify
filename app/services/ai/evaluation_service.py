import logging
import os
import uuid
import asyncio
from typing import List, Dict, Any, Optional
from app.services.ai.model_factory import get_ai_model
from app.services.firestore import save_evaluation_result, get_evaluation_results
from app.models.evaluation import EvaluationStatus, EvaluationStatusResponse

logger = logging.getLogger(__name__)

class EvaluationService:
    """
    Service for evaluating certification readiness
    """
    
    def __init__(self):
        """
        Initialize evaluation service
        """
        self.ai_model = get_ai_model()
        self.active_evaluations = {}  # Track active evaluations
        logger.info("Evaluation service initialized")
    
    async def create_evaluation(
        self,
        organization_id: str,
        certification_types: List[str]
    ) -> str:
        """
        Create a new evaluation record
        
        Args:
            organization_id: Organization ID
            certification_types: List of certification types to evaluate
            
        Returns:
            Evaluation ID
        """
        try:
            logger.info(f"Creating evaluation for organization: {organization_id}")
            
            # Create evaluation record
            evaluation_id = str(uuid.uuid4())
            
            # Initialize evaluation data
            evaluation_data = {
                "id": evaluation_id,
                "organization_id": organization_id,
                "status": EvaluationStatus.PENDING.value,
                "progress": 0.0,
                "certification_types": certification_types,
                "certification_evaluations": []
            }
            
            # Save to Firestore
            await save_evaluation_result(evaluation_data)
            
            logger.info(f"Created evaluation with ID: {evaluation_id}")
            return evaluation_id
        except Exception as e:
            logger.error(f"Error creating evaluation: {str(e)}", exc_info=True)
            raise
    
    async def run_evaluation(
        self,
        organization_id: str,
        evaluation_id: str,
        certification_types: List[str]
    ):
        """
        Run the evaluation process
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            certification_types: List of certification types to evaluate
        """
        try:
            logger.info(f"Starting evaluation process for: {evaluation_id}")
            
            # Update status to in progress
            evaluation_data = {
                "id": evaluation_id,
                "organization_id": organization_id,
                "status": EvaluationStatus.IN_PROGRESS.value,
                "progress": 0.0,
                "certification_types": certification_types,
                "certification_evaluations": []
            }
            
            await save_evaluation_result(evaluation_data)
            
            # Track active evaluation
            self.active_evaluations[evaluation_id] = {
                "organization_id": organization_id,
                "progress": 0.0,
                "status": EvaluationStatus.IN_PROGRESS.value
            }
            
            # Process each certification type
            total_certifications = len(certification_types)
            certification_evaluations = []
            
            for i, cert_type in enumerate(certification_types):
                try:
                    logger.info(f"Evaluating certification: {cert_type} for evaluation: {evaluation_id}")
                    
                    # Generate evaluation for this certification type
                    cert_evaluation = await self.ai_model.evaluate_certification(
                        organization_id=organization_id,
                        certification_type=cert_type
                    )
                    
                    certification_evaluations.append(cert_evaluation)
                    
                    # Update progress
                    progress = ((i + 1) / total_certifications) * 100
                    self.active_evaluations[evaluation_id]["progress"] = progress
                    
                    # Update evaluation data
                    evaluation_data = {
                        "id": evaluation_id,
                        "organization_id": organization_id,
                        "status": EvaluationStatus.IN_PROGRESS.value,
                        "progress": progress,
                        "certification_types": certification_types,
                        "certification_evaluations": certification_evaluations
                    }
                    
                    await save_evaluation_result(evaluation_data)
                    
                except Exception as e:
                    logger.error(f"Error evaluating certification {cert_type}: {str(e)}", exc_info=True)
                    # Continue with next certification type
            
            # Update status to completed
            evaluation_data = {
                "id": evaluation_id,
                "organization_id": organization_id,
                "status": EvaluationStatus.COMPLETED.value,
                "progress": 100.0,
                "certification_types": certification_types,
                "certification_evaluations": certification_evaluations,
                "completed_at": None  # Will be set by Firestore
            }
            
            await save_evaluation_result(evaluation_data)
            
            # Update tracking
            self.active_evaluations[evaluation_id]["status"] = EvaluationStatus.COMPLETED.value
            self.active_evaluations[evaluation_id]["progress"] = 100.0
            
            logger.info(f"Completed evaluation: {evaluation_id}")
            
        except Exception as e:
            logger.error(f"Error running evaluation: {str(e)}", exc_info=True)
            
            # Update status to failed
            try:
                evaluation_data = {
                    "id": evaluation_id,
                    "organization_id": organization_id,
                    "status": EvaluationStatus.FAILED.value,
                    "progress": self.active_evaluations.get(evaluation_id, {}).get("progress", 0.0),
                    "certification_types": certification_types,
                    "certification_evaluations": []
                }
                
                await save_evaluation_result(evaluation_data)
                
                if evaluation_id in self.active_evaluations:
                    self.active_evaluations[evaluation_id]["status"] = EvaluationStatus.FAILED.value
            except Exception as inner_e:
                logger.error(f"Error updating failed evaluation: {str(inner_e)}", exc_info=True)
    
    async def get_evaluation_status(
        self,
        organization_id: str,
        evaluation_id: str
    ) -> Optional[EvaluationStatusResponse]:
        """
        Get the status of an evaluation
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            
        Returns:
            EvaluationStatus object or None if not found
        """
        try:
            logger.info(f"Getting status for evaluation: {evaluation_id}")
            
            # Check active evaluations first
            if evaluation_id in self.active_evaluations:
                active_eval = self.active_evaluations[evaluation_id]
                
                if active_eval["organization_id"] != organization_id:
                    logger.warning(f"Organization ID mismatch for evaluation: {evaluation_id}")
                    return None
                
                return EvaluationStatusResponse(
                    organization_id=organization_id,
                    evaluation_id=evaluation_id,
                    status=active_eval["status"],
                    progress=active_eval["progress"]
                )
            
            # Otherwise, get from Firestore
            evaluation = await get_evaluation_results(organization_id, evaluation_id)
            
            if not evaluation:
                return None
            
            return EvaluationStatusResponse(
                organization_id=organization_id,
                evaluation_id=evaluation_id,
                status=evaluation["status"],
                progress=evaluation["progress"]
            )
        except Exception as e:
            logger.error(f"Error getting evaluation status: {str(e)}", exc_info=True)
            raise
    
    async def get_evaluation_results(
        self,
        organization_id: str,
        evaluation_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get the results of an evaluation
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            
        Returns:
            Evaluation results or None if not found
        """
        try:
            logger.info(f"Getting results for evaluation: {evaluation_id}")
            
            # Get from Firestore
            evaluation = await get_evaluation_results(organization_id, evaluation_id)
            
            if not evaluation:
                return None
            
            # Only return results if evaluation is completed
            if evaluation["status"] != EvaluationStatus.COMPLETED.value:
                logger.warning(f"Evaluation not completed: {evaluation_id}")
                return {
                    "status": evaluation["status"],
                    "progress": evaluation["progress"],
                    "message": "Evaluation not completed"
                }
            
            return evaluation
        except Exception as e:
            logger.error(f"Error getting evaluation results: {str(e)}", exc_info=True)
            raise 