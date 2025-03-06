from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class LLMRequest(BaseModel):
    """
    Request model for LLM API calls.
    """
    prompt: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.7

class LLMResponse(BaseModel):
    """
    Response model for LLM API calls.
    """
    text: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
