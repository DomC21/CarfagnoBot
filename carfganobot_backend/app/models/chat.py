from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []
    selected_topic: Optional[str] = None

class TopicRequest(BaseModel):
    topic_id: str

class ChatResponse(BaseModel):
    message: str
    disclaimer: str
    suggested_topics: Optional[List[Dict[str, Any]]] = None
