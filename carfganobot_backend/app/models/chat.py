from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []
    selected_topic: Optional[str] = None
    user_id: Optional[int] = None

class TopicRequest(BaseModel):
    topic_id: str
    user_id: Optional[int] = None

class EducationalLink(BaseModel):
    title: str
    description: str
    url: str

class ChatResponse(BaseModel):
    message: str
    disclaimer: str
    suggested_topics: Optional[List[Dict[str, Any]]] = None
    educational_links: Optional[List[EducationalLink]] = None
    follow_up_questions: Optional[List[str]] = None
