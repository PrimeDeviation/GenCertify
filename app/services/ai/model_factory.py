import logging
import os
from typing import Dict, Any, Optional, List
import json

logger = logging.getLogger(__name__)

# Get model provider from environment variable
MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "openai")

class BaseAIModel:
    """
    Base class for AI model integration
    """
    
    async def generate_chat_response(
        self,
        message: str,
        organization_id: str,
        session_id: str
    ) -> str:
        """
        Generate a response to a chat message
        
        Args:
            message: User message
            organization_id: Organization ID
            session_id: Chat session ID
            
        Returns:
            AI response text
        """
        raise NotImplementedError("Subclasses must implement generate_chat_response")
    
    async def evaluate_certification(
        self,
        organization_id: str,
        certification_type: str
    ) -> Dict[str, Any]:
        """
        Evaluate certification readiness
        
        Args:
            organization_id: Organization ID
            certification_type: Certification type
            
        Returns:
            Certification evaluation data
        """
        raise NotImplementedError("Subclasses must implement evaluate_certification")
    
    async def generate_document(
        self,
        organization_id: str,
        evaluation_id: str,
        document_type: str,
        evaluation_data: Dict[str, Any]
    ) -> str:
        """
        Generate a compliance document
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            document_type: Document type
            evaluation_data: Evaluation data
            
        Returns:
            Document content
        """
        raise NotImplementedError("Subclasses must implement generate_document")

class OpenAIModel(BaseAIModel):
    """
    OpenAI model integration
    """
    
    def __init__(self):
        """
        Initialize OpenAI model
        """
        try:
            import openai
            
            # Initialize OpenAI client
            self.client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Get model name from environment variable
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
            
            logger.info(f"Initialized OpenAI model: {self.model}")
        except ImportError:
            logger.error("OpenAI package not installed", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error initializing OpenAI model: {str(e)}", exc_info=True)
            raise
    
    async def generate_chat_response(
        self,
        message: str,
        organization_id: str,
        session_id: str
    ) -> str:
        """
        Generate a response to a chat message using OpenAI
        
        Args:
            message: User message
            organization_id: Organization ID
            session_id: Chat session ID
            
        Returns:
            AI response text
        """
        try:
            logger.info(f"Generating chat response with OpenAI for session: {session_id}")
            
            # Create messages
            messages = [
                {"role": "system", "content": "You are a helpful assistant for evaluating certification readiness."},
                {"role": "user", "content": message}
            ]
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            logger.info(f"Generated response for session: {session_id}")
            return response_text
        except Exception as e:
            logger.error(f"Error generating chat response with OpenAI: {str(e)}", exc_info=True)
            raise
    
    async def evaluate_certification(
        self,
        organization_id: str,
        certification_type: str
    ) -> Dict[str, Any]:
        """
        Evaluate certification readiness using OpenAI
        
        Args:
            organization_id: Organization ID
            certification_type: Certification type
            
        Returns:
            Certification evaluation data
        """
        try:
            logger.info(f"Evaluating certification {certification_type} with OpenAI for organization: {organization_id}")
            
            # In a real implementation, we would:
            # 1. Retrieve organization data
            # 2. Retrieve uploaded documents
            # 3. Format data for the AI model
            # 4. Generate evaluation
            
            # For now, return a mock evaluation
            mock_evaluation = {
                "certification_type": certification_type,
                "overall_score": 75.5,
                "requirement_evaluations": [
                    {
                        "requirement_id": "REQ-001",
                        "name": "Information Security Policy",
                        "description": "Organization must have a documented information security policy",
                        "category": "Policies",
                        "certification_type": certification_type,
                        "compliance_score": 80.0,
                        "findings": ["Policy exists but needs updating"],
                        "recommendations": ["Update policy to include latest requirements"]
                    }
                ],
                "summary": "Organization is generally well-prepared but has some gaps to address",
                "strengths": ["Good documentation", "Strong access controls"],
                "weaknesses": ["Outdated policies", "Incomplete risk assessment"],
                "recommendations": ["Update information security policy", "Complete risk assessment"]
            }
            
            logger.info(f"Completed evaluation for certification: {certification_type}")
            return mock_evaluation
        except Exception as e:
            logger.error(f"Error evaluating certification with OpenAI: {str(e)}", exc_info=True)
            raise
    
    async def generate_document(
        self,
        organization_id: str,
        evaluation_id: str,
        document_type: str,
        evaluation_data: Dict[str, Any]
    ) -> str:
        """
        Generate a compliance document using OpenAI
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            document_type: Document type
            evaluation_data: Evaluation data
            
        Returns:
            Document content
        """
        try:
            logger.info(f"Generating document {document_type} with OpenAI for organization: {organization_id}")
            
            # In a real implementation, we would:
            # 1. Format evaluation data for the AI model
            # 2. Generate document content
            
            # For now, return a mock document
            mock_document = f"""
            # {document_type.replace('_', ' ').title()}
            
            ## Introduction
            
            This document outlines the {document_type.replace('_', ' ')} for [Organization Name].
            
            ## Purpose
            
            The purpose of this document is to establish guidelines and procedures for {document_type.replace('_', ' ')}.
            
            ## Scope
            
            This policy applies to all employees, contractors, and third parties who have access to [Organization Name] systems and data.
            
            ## Policy
            
            1. [Organization Name] shall implement and maintain appropriate {document_type.replace('_', ' ')} controls.
            2. All employees shall receive training on {document_type.replace('_', ' ')}.
            3. Regular audits shall be conducted to ensure compliance with this policy.
            
            ## Procedures
            
            1. Procedure 1
            2. Procedure 2
            3. Procedure 3
            
            ## Responsibilities
            
            - Management: Ensure resources are available for implementation
            - IT Department: Implement technical controls
            - Employees: Comply with policy requirements
            
            ## References
            
            - ISO 27001
            - NIST Cybersecurity Framework
            - GDPR
            
            ## Document Control
            
            - Version: 1.0
            - Date: [Current Date]
            - Approved by: [Approver Name]
            """
            
            logger.info(f"Generated document: {document_type}")
            return mock_document
        except Exception as e:
            logger.error(f"Error generating document with OpenAI: {str(e)}", exc_info=True)
            raise

class AnthropicModel(BaseAIModel):
    """
    Anthropic model integration
    """
    
    def __init__(self):
        """
        Initialize Anthropic model
        """
        try:
            import anthropic
            
            # Initialize Anthropic client
            self.client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            
            # Get model name from environment variable
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-2")
            
            logger.info(f"Initialized Anthropic model: {self.model}")
        except ImportError:
            logger.error("Anthropic package not installed", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error initializing Anthropic model: {str(e)}", exc_info=True)
            raise
    
    async def generate_chat_response(
        self,
        message: str,
        organization_id: str,
        session_id: str
    ) -> str:
        """
        Generate a response to a chat message using Anthropic
        
        Args:
            message: User message
            organization_id: Organization ID
            session_id: Chat session ID
            
        Returns:
            AI response text
        """
        try:
            logger.info(f"Generating chat response with Anthropic for session: {session_id}")
            
            # Generate response
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system="You are a helpful assistant for evaluating certification readiness.",
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            
            # Extract response text
            response_text = response.content[0].text
            
            logger.info(f"Generated response for session: {session_id}")
            return response_text
        except Exception as e:
            logger.error(f"Error generating chat response with Anthropic: {str(e)}", exc_info=True)
            raise
    
    async def evaluate_certification(
        self,
        organization_id: str,
        certification_type: str
    ) -> Dict[str, Any]:
        """
        Evaluate certification readiness using Anthropic
        
        Args:
            organization_id: Organization ID
            certification_type: Certification type
            
        Returns:
            Certification evaluation data
        """
        # Implementation similar to OpenAI model
        try:
            logger.info(f"Evaluating certification {certification_type} with Anthropic for organization: {organization_id}")
            
            # Mock evaluation (same as OpenAI for now)
            mock_evaluation = {
                "certification_type": certification_type,
                "overall_score": 75.5,
                "requirement_evaluations": [
                    {
                        "requirement_id": "REQ-001",
                        "name": "Information Security Policy",
                        "description": "Organization must have a documented information security policy",
                        "category": "Policies",
                        "certification_type": certification_type,
                        "compliance_score": 80.0,
                        "findings": ["Policy exists but needs updating"],
                        "recommendations": ["Update policy to include latest requirements"]
                    }
                ],
                "summary": "Organization is generally well-prepared but has some gaps to address",
                "strengths": ["Good documentation", "Strong access controls"],
                "weaknesses": ["Outdated policies", "Incomplete risk assessment"],
                "recommendations": ["Update information security policy", "Complete risk assessment"]
            }
            
            logger.info(f"Completed evaluation for certification: {certification_type}")
            return mock_evaluation
        except Exception as e:
            logger.error(f"Error evaluating certification with Anthropic: {str(e)}", exc_info=True)
            raise
    
    async def generate_document(
        self,
        organization_id: str,
        evaluation_id: str,
        document_type: str,
        evaluation_data: Dict[str, Any]
    ) -> str:
        """
        Generate a compliance document using Anthropic
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            document_type: Document type
            evaluation_data: Evaluation data
            
        Returns:
            Document content
        """
        # Implementation similar to OpenAI model
        try:
            logger.info(f"Generating document {document_type} with Anthropic for organization: {organization_id}")
            
            # Mock document (same as OpenAI for now)
            mock_document = f"""
            # {document_type.replace('_', ' ').title()}
            
            ## Introduction
            
            This document outlines the {document_type.replace('_', ' ')} for [Organization Name].
            
            ## Purpose
            
            The purpose of this document is to establish guidelines and procedures for {document_type.replace('_', ' ')}.
            
            ## Scope
            
            This policy applies to all employees, contractors, and third parties who have access to [Organization Name] systems and data.
            
            ## Policy
            
            1. [Organization Name] shall implement and maintain appropriate {document_type.replace('_', ' ')} controls.
            2. All employees shall receive training on {document_type.replace('_', ' ')}.
            3. Regular audits shall be conducted to ensure compliance with this policy.
            
            ## Procedures
            
            1. Procedure 1
            2. Procedure 2
            3. Procedure 3
            
            ## Responsibilities
            
            - Management: Ensure resources are available for implementation
            - IT Department: Implement technical controls
            - Employees: Comply with policy requirements
            
            ## References
            
            - ISO 27001
            - NIST Cybersecurity Framework
            - GDPR
            
            ## Document Control
            
            - Version: 1.0
            - Date: [Current Date]
            - Approved by: [Approver Name]
            """
            
            logger.info(f"Generated document: {document_type}")
            return mock_document
        except Exception as e:
            logger.error(f"Error generating document with Anthropic: {str(e)}", exc_info=True)
            raise

class VertexAIModel(BaseAIModel):
    """
    Google Vertex AI model integration
    """
    
    def __init__(self):
        """
        Initialize Vertex AI model
        """
        try:
            from google.cloud import aiplatform
            
            # Initialize Vertex AI
            aiplatform.init(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("VERTEX_AI_LOCATION", "us-central1")
            )
            
            # Get model ID from environment variable
            self.model_id = os.getenv("VERTEX_AI_MODEL_ID", "text-bison@001")
            
            logger.info(f"Initialized Vertex AI model: {self.model_id}")
        except ImportError:
            logger.error("Google Cloud AI Platform package not installed", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error initializing Vertex AI model: {str(e)}", exc_info=True)
            raise
    
    async def generate_chat_response(
        self,
        message: str,
        organization_id: str,
        session_id: str
    ) -> str:
        """
        Generate a response to a chat message using Vertex AI
        
        Args:
            message: User message
            organization_id: Organization ID
            session_id: Chat session ID
            
        Returns:
            AI response text
        """
        try:
            logger.info(f"Generating chat response with Vertex AI for session: {session_id}")
            
            from google.cloud import aiplatform
            
            # Create prompt
            prompt = f"""
            You are a helpful assistant for evaluating certification readiness.
            
            User: {message}
            
            Assistant:
            """
            
            # Get model
            model = aiplatform.TextGenerationModel.from_pretrained(self.model_id)
            
            # Generate response
            response = model.predict(prompt=prompt, max_output_tokens=1000, temperature=0.7)
            
            # Extract response text
            response_text = response.text
            
            logger.info(f"Generated response for session: {session_id}")
            return response_text
        except Exception as e:
            logger.error(f"Error generating chat response with Vertex AI: {str(e)}", exc_info=True)
            raise
    
    async def evaluate_certification(
        self,
        organization_id: str,
        certification_type: str
    ) -> Dict[str, Any]:
        """
        Evaluate certification readiness using Vertex AI
        
        Args:
            organization_id: Organization ID
            certification_type: Certification type
            
        Returns:
            Certification evaluation data
        """
        # Implementation similar to other models
        try:
            logger.info(f"Evaluating certification {certification_type} with Vertex AI for organization: {organization_id}")
            
            # Mock evaluation (same as other models for now)
            mock_evaluation = {
                "certification_type": certification_type,
                "overall_score": 75.5,
                "requirement_evaluations": [
                    {
                        "requirement_id": "REQ-001",
                        "name": "Information Security Policy",
                        "description": "Organization must have a documented information security policy",
                        "category": "Policies",
                        "certification_type": certification_type,
                        "compliance_score": 80.0,
                        "findings": ["Policy exists but needs updating"],
                        "recommendations": ["Update policy to include latest requirements"]
                    }
                ],
                "summary": "Organization is generally well-prepared but has some gaps to address",
                "strengths": ["Good documentation", "Strong access controls"],
                "weaknesses": ["Outdated policies", "Incomplete risk assessment"],
                "recommendations": ["Update information security policy", "Complete risk assessment"]
            }
            
            logger.info(f"Completed evaluation for certification: {certification_type}")
            return mock_evaluation
        except Exception as e:
            logger.error(f"Error evaluating certification with Vertex AI: {str(e)}", exc_info=True)
            raise
    
    async def generate_document(
        self,
        organization_id: str,
        evaluation_id: str,
        document_type: str,
        evaluation_data: Dict[str, Any]
    ) -> str:
        """
        Generate a compliance document using Vertex AI
        
        Args:
            organization_id: Organization ID
            evaluation_id: Evaluation ID
            document_type: Document type
            evaluation_data: Evaluation data
            
        Returns:
            Document content
        """
        # Implementation similar to other models
        try:
            logger.info(f"Generating document {document_type} with Vertex AI for organization: {organization_id}")
            
            # Mock document (same as other models for now)
            mock_document = f"""
            # {document_type.replace('_', ' ').title()}
            
            ## Introduction
            
            This document outlines the {document_type.replace('_', ' ')} for [Organization Name].
            
            ## Purpose
            
            The purpose of this document is to establish guidelines and procedures for {document_type.replace('_', ' ')}.
            
            ## Scope
            
            This policy applies to all employees, contractors, and third parties who have access to [Organization Name] systems and data.
            
            ## Policy
            
            1. [Organization Name] shall implement and maintain appropriate {document_type.replace('_', ' ')} controls.
            2. All employees shall receive training on {document_type.replace('_', ' ')}.
            3. Regular audits shall be conducted to ensure compliance with this policy.
            
            ## Procedures
            
            1. Procedure 1
            2. Procedure 2
            3. Procedure 3
            
            ## Responsibilities
            
            - Management: Ensure resources are available for implementation
            - IT Department: Implement technical controls
            - Employees: Comply with policy requirements
            
            ## References
            
            - ISO 27001
            - NIST Cybersecurity Framework
            - GDPR
            
            ## Document Control
            
            - Version: 1.0
            - Date: [Current Date]
            - Approved by: [Approver Name]
            """
            
            logger.info(f"Generated document: {document_type}")
            return mock_document
        except Exception as e:
            logger.error(f"Error generating document with Vertex AI: {str(e)}", exc_info=True)
            raise

def get_ai_model() -> BaseAIModel:
    """
    Get the appropriate AI model based on configuration
    
    Returns:
        AI model instance
    """
    try:
        logger.info(f"Getting AI model for provider: {MODEL_PROVIDER}")
        
        if MODEL_PROVIDER.lower() == "openai":
            return OpenAIModel()
        elif MODEL_PROVIDER.lower() == "anthropic":
            return AnthropicModel()
        elif MODEL_PROVIDER.lower() == "vertexai":
            return VertexAIModel()
        else:
            logger.warning(f"Unknown model provider: {MODEL_PROVIDER}, defaulting to OpenAI")
            return OpenAIModel()
    except Exception as e:
        logger.error(f"Error getting AI model: {str(e)}", exc_info=True)
        raise 