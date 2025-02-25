import logging
import os
from typing import Dict, List, Any, Optional, Union
from google.cloud import firestore
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

# Initialize Firestore client with error handling for development
try:
    # If FIRESTORE_EMULATOR_HOST is set, it will connect to the emulator
    db = firestore.Client()
    logger.info("Connected to Firestore successfully")
except Exception as e:
    logger.warning(f"Failed to connect to Firestore: {e}")
    logger.warning("Running in development mode with mock Firestore")
    db = None

# Collection names from environment variables
COLLECTION_USERS = os.getenv("FIRESTORE_COLLECTION_USERS", "users")
COLLECTION_CERTIFICATIONS = os.getenv("FIRESTORE_COLLECTION_CERTIFICATIONS", "certifications")
COLLECTION_EVALUATIONS = os.getenv("FIRESTORE_COLLECTION_EVALUATIONS", "evaluations")
COLLECTION_DOCUMENTS = os.getenv("FIRESTORE_COLLECTION_DOCUMENTS", "documents")
COLLECTION_CHAT_SESSIONS = "chat_sessions"

async def save_organization_data(organization_data: Dict[str, Any]) -> str:
    """
    Save organization data to Firestore
    
    Args:
        organization_data: Organization data dictionary
        
    Returns:
        Organization ID
    """
    try:
        # Generate ID if not provided
        org_id = organization_data.get("id", str(uuid.uuid4()))
        
        if db is None:
            # Mock implementation for development
            logger.info(f"[MOCK] Saved organization data with ID: {org_id}")
            return org_id
        
        # Add timestamps
        organization_data["created_at"] = firestore.SERVER_TIMESTAMP
        organization_data["updated_at"] = firestore.SERVER_TIMESTAMP
        
        # Save to Firestore
        doc_ref = db.collection(COLLECTION_USERS).document(org_id)
        doc_ref.set(organization_data)
        
        logger.info(f"Saved organization data with ID: {org_id}")
        return org_id
    except Exception as e:
        logger.error(f"Error saving organization data: {str(e)}", exc_info=True)
        raise

async def get_organization_data(organization_id: str) -> Optional[Dict[str, Any]]:
    """
    Get organization data from Firestore
    
    Args:
        organization_id: Organization ID
        
    Returns:
        Organization data dictionary or None if not found
    """
    try:
        if db is None:
            # Mock implementation for development
            mock_data = {
                "id": organization_id,
                "name": "Mock Organization",
                "email": "mock@example.com",
                "industry": "Technology",
                "size": "Medium",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            logger.info(f"[MOCK] Retrieved organization data for ID: {organization_id}")
            return mock_data
            
        doc_ref = db.collection(COLLECTION_USERS).document(organization_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            logger.warning(f"Organization not found: {organization_id}")
            return None
        
        # Get data and add ID
        data = doc.to_dict()
        data["id"] = organization_id
        
        logger.info(f"Retrieved organization data for ID: {organization_id}")
        return data
    except Exception as e:
        logger.error(f"Error getting organization data: {str(e)}", exc_info=True)
        raise

async def save_evaluation_result(evaluation_data: Dict[str, Any]) -> str:
    """
    Save evaluation result to Firestore
    
    Args:
        evaluation_data: Evaluation data dictionary
        
    Returns:
        Evaluation ID
    """
    try:
        # Add timestamps
        evaluation_data["created_at"] = firestore.SERVER_TIMESTAMP
        evaluation_data["updated_at"] = firestore.SERVER_TIMESTAMP
        
        # Generate ID if not provided
        evaluation_id = evaluation_data.get("id", str(uuid.uuid4()))
        
        # Save to Firestore
        doc_ref = db.collection(COLLECTION_EVALUATIONS).document(evaluation_id)
        doc_ref.set(evaluation_data)
        
        logger.info(f"Saved evaluation result with ID: {evaluation_id}")
        return evaluation_id
    except Exception as e:
        logger.error(f"Error saving evaluation result: {str(e)}", exc_info=True)
        raise

async def get_evaluation_results(organization_id: str, evaluation_id: str) -> Optional[Dict[str, Any]]:
    """
    Get evaluation results from Firestore
    
    Args:
        organization_id: Organization ID
        evaluation_id: Evaluation ID
        
    Returns:
        Evaluation data dictionary or None if not found
    """
    try:
        doc_ref = db.collection(COLLECTION_EVALUATIONS).document(evaluation_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            logger.warning(f"Evaluation not found: {evaluation_id}")
            return None
        
        # Get data and add ID
        data = doc.to_dict()
        
        # Verify organization ID
        if data.get("organization_id") != organization_id:
            logger.warning(f"Evaluation {evaluation_id} does not belong to organization {organization_id}")
            return None
        
        data["id"] = evaluation_id
        
        logger.info(f"Retrieved evaluation results for ID: {evaluation_id}")
        return data
    except Exception as e:
        logger.error(f"Error getting evaluation results: {str(e)}", exc_info=True)
        raise

async def save_document_generation(document_data: Dict[str, Any]) -> str:
    """
    Save document generation data to Firestore
    
    Args:
        document_data: Document generation data dictionary
        
    Returns:
        Document generation ID
    """
    try:
        # Add timestamps
        document_data["created_at"] = firestore.SERVER_TIMESTAMP
        document_data["updated_at"] = firestore.SERVER_TIMESTAMP
        
        # Generate ID if not provided
        document_id = document_data.get("id", str(uuid.uuid4()))
        
        # Save to Firestore
        doc_ref = db.collection(COLLECTION_DOCUMENTS).document(document_id)
        doc_ref.set(document_data)
        
        logger.info(f"Saved document generation with ID: {document_id}")
        return document_id
    except Exception as e:
        logger.error(f"Error saving document generation: {str(e)}", exc_info=True)
        raise

async def save_chat_message(organization_id: str, session_id: str, user_message: str, ai_response: str) -> str:
    """
    Save chat messages to Firestore
    
    Args:
        organization_id: Organization ID
        session_id: Chat session ID
        user_message: User message
        ai_response: AI response
        
    Returns:
        Session ID
    """
    try:
        # Get or create session
        session_ref = db.collection(COLLECTION_CHAT_SESSIONS).document(session_id)
        session = session_ref.get()
        
        # Current timestamp
        now = firestore.SERVER_TIMESTAMP
        
        if not session.exists:
            # Create new session
            session_data = {
                "organization_id": organization_id,
                "messages": [
                    {
                        "role": "user",
                        "content": user_message,
                        "timestamp": now
                    },
                    {
                        "role": "assistant",
                        "content": ai_response,
                        "timestamp": now
                    }
                ],
                "created_at": now,
                "updated_at": now
            }
            session_ref.set(session_data)
        else:
            # Update existing session
            session_data = session.to_dict()
            session_data["messages"].append({
                "role": "user",
                "content": user_message,
                "timestamp": now
            })
            session_data["messages"].append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": now
            })
            session_data["updated_at"] = now
            session_ref.update(session_data)
        
        logger.info(f"Saved chat messages for session: {session_id}")
        return session_id
    except Exception as e:
        logger.error(f"Error saving chat messages: {str(e)}", exc_info=True)
        raise

async def get_chat_history(organization_id: str, session_id: str) -> Optional[Dict[str, Any]]:
    """
    Get chat history from Firestore
    
    Args:
        organization_id: Organization ID
        session_id: Chat session ID
        
    Returns:
        Chat session data dictionary or None if not found
    """
    try:
        doc_ref = db.collection(COLLECTION_CHAT_SESSIONS).document(session_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            logger.warning(f"Chat session not found: {session_id}")
            return None
        
        # Get data and add ID
        data = doc.to_dict()
        
        # Verify organization ID
        if data.get("organization_id") != organization_id:
            logger.warning(f"Chat session {session_id} does not belong to organization {organization_id}")
            return None
        
        data["id"] = session_id
        
        logger.info(f"Retrieved chat history for session: {session_id}")
        return data
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}", exc_info=True)
        raise 