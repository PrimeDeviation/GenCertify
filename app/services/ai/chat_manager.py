import logging
import os
import uuid
from typing import List, Dict, Any, Optional
from app.services.ai.model_factory import get_ai_model
from app.models.chat import ChatResponse

logger = logging.getLogger(__name__)

class ChatManager:
    """
    Manager for handling chat interactions with AI models
    """
    
    def __init__(self):
        """
        Initialize chat manager
        """
        self.ai_model = get_ai_model()
        logger.info("Chat manager initialized")
    
    async def process_message(
        self,
        organization_id: str,
        message: str,
        session_id: Optional[str] = None
    ) -> ChatResponse:
        """
        Process a user message and generate a response
        
        Args:
            organization_id: Organization ID
            message: User message
            session_id: Chat session ID (optional)
            
        Returns:
            ChatResponse object with AI response
        """
        try:
            logger.info(f"Processing message for organization: {organization_id}")
            
            # Generate or use existing session ID
            if not session_id:
                session_id = str(uuid.uuid4())
                logger.info(f"Created new chat session: {session_id}")
            
            # Get chat history if session exists
            # This would be implemented to retrieve history from Firestore
            # and format it for the AI model
            
            # Process message with AI model
            response_text = await self.ai_model.generate_chat_response(
                message=message,
                organization_id=organization_id,
                session_id=session_id
            )
            
            # Create response
            response = ChatResponse(
                message=response_text,
                session_id=session_id,
                metadata={
                    "organization_id": organization_id,
                    "timestamp": None  # Will be set by Firestore
                }
            )
            
            logger.info(f"Generated response for session: {session_id}")
            return response
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            raise 