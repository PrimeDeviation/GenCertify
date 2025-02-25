import logging
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from typing import List, Optional, Dict, Any
from app.services.ai.chat_manager import ChatManager
from app.services.firestore import save_chat_message, get_chat_history
from app.models.chat import ChatMessageRequest as ChatMessage, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize chat manager
chat_manager = ChatManager()

@router.post("/message")
async def send_message(chat_message: ChatMessage) -> ChatResponse:
    """
    Send a message to the chat interface and get a response
    """
    logger.info(f"Received chat message for organization: {chat_message.organization_id}")
    
    try:
        # Process message and get response
        response = await chat_manager.process_message(
            organization_id=chat_message.organization_id,
            message=chat_message.message,
            session_id=chat_message.session_id
        )
        
        # Save message to Firestore
        await save_chat_message(
            organization_id=chat_message.organization_id,
            session_id=response.session_id,
            user_message=chat_message.message,
            ai_response=response.message
        )
        
        return response
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@router.get("/history/{organization_id}/{session_id}")
async def get_chat_session_history(organization_id: str, session_id: str):
    """
    Get chat history for a specific session
    """
    logger.info(f"Fetching chat history for organization: {organization_id}, session: {session_id}")
    
    try:
        # Get chat history from Firestore
        history = await get_chat_history(organization_id, session_id)
        
        return {
            "status": "success",
            "history": history
        }
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")

@router.websocket("/ws/{organization_id}")
async def websocket_endpoint(websocket: WebSocket, organization_id: str):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket.accept()
    session_id = None
    
    try:
        logger.info(f"WebSocket connection established for organization: {organization_id}")
        
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message")
            session_id = data.get("session_id", session_id)
            
            if not message:
                continue
            
            # Process message and get response
            response = await chat_manager.process_message(
                organization_id=organization_id,
                message=message,
                session_id=session_id
            )
            
            # Save message to Firestore
            await save_chat_message(
                organization_id=organization_id,
                session_id=response.session_id,
                user_message=message,
                ai_response=response.message
            )
            
            # Send response back to client
            await websocket.send_json({
                "message": response.message,
                "session_id": response.session_id,
                "metadata": response.metadata
            })
            
            # Update session_id for future messages
            session_id = response.session_id
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for organization: {organization_id}")
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}", exc_info=True)
        await websocket.close() 