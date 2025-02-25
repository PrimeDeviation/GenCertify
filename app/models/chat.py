from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class MessageRole(str, Enum):
    """
    Enum for message roles
    """
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    """
    Model representing a chat message
    """
    id: Optional[str] = Field(None, description="Message ID")
    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(None, description="Message timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ChatSession(BaseModel):
    """
    Model representing a chat session
    """
    id: Optional[str] = Field(None, description="Session ID")
    organization_id: str = Field(..., description="Organization ID")
    messages: List[ChatMessage] = Field([], description="Chat messages")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary for Firestore storage
        """
        data = self.dict(exclude={"id", "created_at", "updated_at"})
        return data
    
    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]) -> "ChatSession":
        """
        Create model from Firestore dictionary
        """
        # Convert Firestore timestamps to datetime objects
        for timestamp_field in ["created_at", "updated_at"]:
            if timestamp_field in data and data[timestamp_field]:
                data[timestamp_field] = data[timestamp_field].datetime
                
        # Convert timestamps in messages
        if "messages" in data:
            for msg in data["messages"]:
                if "timestamp" in msg and msg["timestamp"]:
                    msg["timestamp"] = msg["timestamp"].datetime
            
        return cls(id=id, **data)

# API models to avoid circular imports
class ChatMessageRequest(BaseModel):
    organization_id: str = Field(..., description="Organization ID")
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI response message")
    session_id: str = Field(..., description="Chat session ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata") 