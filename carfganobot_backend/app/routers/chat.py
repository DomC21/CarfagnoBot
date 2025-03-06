from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, TopicRequest, ChatResponse
from app.services.chat_service import get_topic_content, process_chat_message
from app.data.investing_topics import MAIN_TOPICS_LIST, DISCLAIMER

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Process a chat message from the user and return a response.
    """
    try:
        response = process_chat_message(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topic", response_model=ChatResponse)
async def get_topic(request: TopicRequest):
    """
    Get content for a specific investing topic.
    """
    try:
        response = get_topic_content(request.topic_id)
        return response
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Topic {request.topic_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
async def get_topics():
    """
    Get the list of main investing topics.
    """
    return {
        "topics": MAIN_TOPICS_LIST,
        "disclaimer": DISCLAIMER
    }
