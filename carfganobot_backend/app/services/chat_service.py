"""
Service for handling chat functionality and topic navigation.
"""
from app.models.chat import ChatRequest, ChatResponse, Message
from app.models.llm import LLMRequest
from app.data.investing_topics import INVESTING_TOPICS, SUBTOPICS_CONTENT, MAIN_TOPICS_LIST, DISCLAIMER
from app.services.llm_service import generate_response
from typing import List, Dict, Any, Optional

def get_topic_content(topic_id: str) -> ChatResponse:
    """
    Get content for a specific investing topic.
    """
    # Check if topic exists in main topics
    if topic_id in INVESTING_TOPICS:
        topic = INVESTING_TOPICS[topic_id]
        message = f"**{topic['title']}**\n\n{topic['content']}"
        
        # Add subtopics as suggested topics
        suggested_topics = topic.get('subtopics', [])
        
        # Always add a link back to main topics
        suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
        
        return ChatResponse(
            message=message,
            disclaimer=DISCLAIMER,
            suggested_topics=suggested_topics
        )
    
    # Check if it's a subtopic
    elif topic_id in SUBTOPICS_CONTENT:
        content = SUBTOPICS_CONTENT[topic_id]
        
        # Find parent topic to get title
        parent_topic = None
        parent_id = None
        
        for tid, topic in INVESTING_TOPICS.items():
            for subtopic in topic.get('subtopics', []):
                if subtopic['id'] == topic_id:
                    parent_topic = topic['title']
                    parent_id = topic['id']
                    break
            if parent_topic:
                break
        
        title = next((st['title'] for t in INVESTING_TOPICS.values() 
                     for st in t.get('subtopics', []) if st['id'] == topic_id), topic_id)
        
        message = f"**{title}**\n\n{content}"
        
        suggested_topics = [{"id": parent_id, "title": f"Back to {parent_topic}"}] if parent_id else []
        suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
        
        return ChatResponse(
            message=message,
            disclaimer=DISCLAIMER,
            suggested_topics=suggested_topics
        )
    
    # Handle main menu request
    elif topic_id == "main_menu":
        message = "**Welcome to CarfganoBot!**\n\nI'm here to help you learn about investing. Please select a topic you'd like to explore:"
        
        return ChatResponse(
            message=message,
            disclaimer=DISCLAIMER,
            suggested_topics=MAIN_TOPICS_LIST
        )
    
    # Topic not found
    else:
        raise KeyError(f"Topic {topic_id} not found")

def process_chat_message(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message from the user and return a response.
    Uses the LLM service to generate responses for open-ended questions.
    """
    message = request.message
    conversation_history = request.conversation_history
    
    # Convert conversation history to format expected by LLM
    llm_conversation_history = None
    if conversation_history:
        llm_conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history
        ]
    
    # Check for direct topic selection by keyword
    message_lower = message.lower()
    
    # Check for greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
        response = "Hello! I'm CarfganoBot from Carfgano Enterprises, here to help you learn about investing. What topic would you like to explore today?"
        return ChatResponse(
            message=response,
            disclaimer=DISCLAIMER,
            suggested_topics=MAIN_TOPICS_LIST
        )
    
    # Check for direct topic matches
    for topic_id, topic in INVESTING_TOPICS.items():
        topic_keywords = [topic['title'].lower()] + [word.lower() for word in topic_id.split('_')]
        if any(keyword in message_lower for keyword in topic_keywords):
            return get_topic_content(topic_id)
    
    # Check for subtopic matches
    for subtopic_id in SUBTOPICS_CONTENT.keys():
        subtopic_keywords = [subtopic_id.replace('_', ' ').lower()]
        
        # Find the subtopic title
        for topic in INVESTING_TOPICS.values():
            for subtopic in topic.get('subtopics', []):
                if subtopic['id'] == subtopic_id:
                    subtopic_keywords.append(subtopic['title'].lower())
        
        if any(keyword in message_lower for keyword in subtopic_keywords):
            # Create a custom prompt for the LLM
            prompt = f"Explain {subtopic_id.replace('_', ' ')} in investing"
            llm_request = LLMRequest(prompt=prompt, conversation_history=llm_conversation_history)
            llm_response = generate_response(llm_request)
            
            # Find parent topic for navigation
            parent_topic = None
            parent_id = None
            for tid, topic in INVESTING_TOPICS.items():
                for subtopic in topic.get('subtopics', []):
                    if subtopic['id'] == subtopic_id:
                        parent_topic = topic['title']
                        parent_id = topic['id']
                        break
                if parent_topic:
                    break
            
            suggested_topics = [{"id": parent_id, "title": f"Back to {parent_topic}"}] if parent_id else []
            suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
            
            return ChatResponse(
                message=llm_response.text,
                disclaimer=DISCLAIMER,
                suggested_topics=suggested_topics
            )
    
    # For open-ended questions, use the LLM
    llm_request = LLMRequest(prompt=message, conversation_history=llm_conversation_history)
    llm_response = generate_response(llm_request)
    
    # Determine suggested topics based on the content of the response
    suggested_topics = determine_suggested_topics(message_lower, llm_response.text.lower())
    
    return ChatResponse(
        message=llm_response.text,
        disclaimer=DISCLAIMER,
        suggested_topics=suggested_topics
    )

def determine_suggested_topics(user_message: str, response_text: str) -> List[Dict[str, str]]:
    """
    Determine relevant suggested topics based on the user message and response.
    """
    suggested_topics = []
    
    # Check for topic keywords in both user message and response
    topic_keywords = {
        "investing_basics": ["basic", "beginner", "start", "new to investing"],
        "stocks": ["stock", "share", "equity", "dividend"],
        "bonds": ["bond", "fixed income", "debt", "yield", "coupon"],
        "risk_management": ["risk", "diversif", "portfolio", "allocation"],
        "market_analysis": ["analysis", "technical", "fundamental", "chart"],
        "advanced_concepts": ["advanced", "option", "future", "derivative", "alternative"]
    }
    
    # Count keyword matches for each topic
    topic_scores = {topic_id: 0 for topic_id in topic_keywords.keys()}
    
    for topic_id, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in user_message:
                topic_scores[topic_id] += 2  # Higher weight for user message
            if keyword in response_text:
                topic_scores[topic_id] += 1
    
    # Get top 3 topics
    top_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Add suggested topics if they have a score > 0
    for topic_id, score in top_topics:
        if score > 0:
            topic = INVESTING_TOPICS[topic_id]
            suggested_topics.append({"id": topic_id, "title": topic["title"]})
    
    # Always add main menu option
    suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
    
    return suggested_topics
