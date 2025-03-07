from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from enum import Enum

class UserProficiencyLevel(str, Enum):
    """
    Enum for user proficiency levels.
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ConversationMessage(BaseModel):
    """
    Model for a single message in a conversation.
    """
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None

class UserContext(BaseModel):
    """
    Model for user context information.
    """
    user_id: Optional[int] = None
    proficiency_level: Optional[UserProficiencyLevel] = UserProficiencyLevel.BEGINNER
    topics_completed: Optional[List[str]] = []
    quiz_scores: Optional[Dict[str, float]] = {}
    interests: Optional[List[str]] = []
    last_interaction: Optional[str] = None

class LLMRequest(BaseModel):
    """
    Enhanced request model for LLM API calls with user context.
    """
    prompt: str
    conversation_history: Optional[List[ConversationMessage]] = None
    user_context: Optional[UserContext] = None
    max_tokens: Optional[int] = 300  # Increased for more detailed responses
    temperature: Optional[float] = 0.7
    include_follow_up_questions: Optional[bool] = True

class LLMResponse(BaseModel):
    """
    Enhanced response model for LLM API calls with additional educational content.
    """
    text: str
    follow_up_questions: Optional[List[str]] = None
    suggested_topics: Optional[List[Dict[str, str]]] = None
    educational_links: Optional[List[Dict[str, str]]] = None
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
