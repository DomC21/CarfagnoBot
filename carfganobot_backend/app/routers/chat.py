from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, TopicRequest, ChatResponse
from app.services.chat_service import (
    get_topic_content, process_chat_message, get_enhanced_topic_content,
    determine_user_proficiency
)
from app.models.llm import UserProficiencyLevel
from app.data.investing_topics import MAIN_TOPICS_LIST, DISCLAIMER
from app.data.enhanced_investing_topics import ENHANCED_MAIN_TOPICS_LIST, ENHANCED_DISCLAIMER
from typing import Optional
from app.auth.security import get_current_user_optional

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest, current_user: Optional[dict] = Depends(get_current_user_optional)):
    """
    Process a chat message from the user and return a response.
    Uses enhanced AI coaching if user is authenticated.
    """
    try:
        # Add user_id to request if user is authenticated
        if current_user:
            request.user_id = current_user.get("id")
        
        response = process_chat_message(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topic", response_model=ChatResponse)
async def get_topic(request: TopicRequest, current_user: Optional[dict] = Depends(get_current_user_optional)):
    """
    Get content for a specific investing topic.
    Uses enhanced content with proficiency-based responses if user is authenticated.
    """
    try:
        # If user is authenticated, use enhanced topic content
        if current_user:
            user_id = current_user.get("id")
            request.user_id = user_id
            
            # Determine user proficiency level
            proficiency_level = determine_user_proficiency(user_id)
            
            # Get enhanced topic content
            response = get_enhanced_topic_content(request.topic_id, proficiency_level)
        else:
            # Use regular topic content for unauthenticated users
            response = get_topic_content(request.topic_id)
            
        return response
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Topic {request.topic_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
async def get_topics(current_user: Optional[dict] = Depends(get_current_user_optional)):
    """
    Get the list of main investing topics.
    Returns enhanced topics with proficiency-based content if user is authenticated.
    """
    if current_user:
        return {
            "topics": ENHANCED_MAIN_TOPICS_LIST,
            "disclaimer": ENHANCED_DISCLAIMER
        }
    else:
        return {
            "topics": MAIN_TOPICS_LIST,
            "disclaimer": DISCLAIMER
        }

@router.get("/proficiency")
async def get_user_proficiency(current_user: dict = Depends(get_current_user_optional)):
    """
    Get the user's current proficiency level.
    Requires authentication.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    user_id = current_user.get("id")
    proficiency_level = determine_user_proficiency(user_id)
    
    return {
        "user_id": user_id,
        "proficiency_level": proficiency_level.value,
        "description": get_proficiency_description(proficiency_level)
    }

def get_proficiency_description(level: UserProficiencyLevel) -> str:
    """
    Get a description of the user's proficiency level.
    """
    descriptions = {
        UserProficiencyLevel.BEGINNER: "You're just starting your investing journey. Focus on learning the fundamentals.",
        UserProficiencyLevel.INTERMEDIATE: "You have a good grasp of investing basics. Ready to explore more complex concepts.",
        UserProficiencyLevel.ADVANCED: "You have a strong understanding of investing. Explore advanced strategies and analysis techniques."
    }
    
    return descriptions.get(level, "Unknown proficiency level")
