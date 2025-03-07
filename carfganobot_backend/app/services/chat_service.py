"""
Service for handling chat functionality and topic navigation with enhanced AI coaching capabilities.
"""
from app.models.chat import ChatRequest, ChatResponse
from app.models.llm import LLMRequest, ConversationMessage, UserContext, UserProficiencyLevel
from app.data.investing_topics import INVESTING_TOPICS, SUBTOPICS_CONTENT, MAIN_TOPICS_LIST, DISCLAIMER
from app.data.enhanced_investing_topics import ENHANCED_INVESTING_TOPICS, ENHANCED_MAIN_TOPICS_LIST, ENHANCED_DISCLAIMER
from app.services.llm_service import generate_response
from typing import List, Dict, Optional
from datetime import datetime


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

        suggested_topics = [{"id": parent_id,
                             "title": f"Back to {parent_topic}"}] if parent_id else []
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


def get_enhanced_topic_content(topic_id: str, proficiency_level: UserProficiencyLevel) -> ChatResponse:
    """
    Get enhanced content for a specific investing topic based on user proficiency level.
    """
    # Convert proficiency level to string for content lookup
    prof_level = proficiency_level.value
    
    # Check if topic exists in enhanced topics
    if topic_id in ENHANCED_INVESTING_TOPICS:
        topic = ENHANCED_INVESTING_TOPICS[topic_id]
        
        # Get content for appropriate proficiency level
        if prof_level in topic['content']:
            content = topic['content'][prof_level]
        else:
            # Fallback to beginner if specific level not available
            content = topic['content'].get('beginner', topic['content'].get(list(topic['content'].keys())[0]))
        
        message = f"**{topic['title']}**\n\n{content}"

        # Add subtopics as suggested topics
        suggested_topics = topic.get('subtopics', [])

        # Add educational links if available
        educational_links = None
        if 'educational_links' in topic:
            educational_links = [
                link for link in topic['educational_links']
                if link.get('difficulty', 'beginner') == prof_level or not link.get('difficulty')
            ]
            
            # If no links match the proficiency level, include beginner links
            if not educational_links and prof_level != 'beginner':
                educational_links = [
                    link for link in topic['educational_links']
                    if link.get('difficulty', 'beginner') == 'beginner'
                ]

        # Add follow-up questions if available
        follow_up_questions = []
        if 'follow_up_questions' in topic:
            import random
            follow_up_questions = random.sample(
                topic['follow_up_questions'],
                min(3, len(topic['follow_up_questions']))
            )
            
            # Add follow-up questions as suggested topics
            for i, question in enumerate(follow_up_questions):
                suggested_topics.append({
                    "id": f"follow_up_{i}",
                    "title": question,
                    "is_question": True
                })

        # Always add a link back to main topics
        suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})

        return ChatResponse(
            message=message,
            disclaimer=ENHANCED_DISCLAIMER,
            suggested_topics=suggested_topics,
            educational_links=educational_links
        )
    
    # If not found in enhanced topics, fall back to regular topics
    return get_topic_content(topic_id)


def determine_user_proficiency(user_id: int) -> UserProficiencyLevel:
    """
    Determine the user's proficiency level based on their quiz scores and topic completions.
    In a real implementation, this would query the database for the user's quiz results and topic progress.
    """
    # Mock implementation - in a real app, we would query the database
    # For now, return a default proficiency level
    return UserProficiencyLevel.BEGINNER


def get_completed_topics(user_id: int) -> List[str]:
    """
    Get the list of topics that the user has completed.
    In a real implementation, this would query the database for the user's topic progress.
    """
    # Mock implementation - in a real app, we would query the database
    return []


def get_user_quiz_scores(user_id: int) -> Dict[str, float]:
    """
    Get the user's quiz scores for different topics.
    In a real implementation, this would query the database for the user's quiz results.
    """
    # Mock implementation - in a real app, we would query the database
    return {}


def get_user_interests(user_id: int) -> List[str]:
    """
    Get the user's interests based on their interactions with the app.
    In a real implementation, this would analyze the user's behavior and quiz results.
    """
    # Mock implementation - in a real app, we would query the database
    return []


def process_chat_message(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message from the user and return a response.
    Uses the enhanced LLM service to generate personalized responses based on user context.
    """
    message = request.message
    conversation_history = request.conversation_history
    user_id = request.user_id
    
    # Create user context if user is authenticated
    user_context = None
    if user_id:
        # In a real implementation, we would fetch user data from the database
        # For now, we'll create a simple user context
        user_context = UserContext(
            user_id=user_id,
            proficiency_level=determine_user_proficiency(user_id),
            topics_completed=get_completed_topics(user_id),
            quiz_scores=get_user_quiz_scores(user_id),
            interests=get_user_interests(user_id),
            last_interaction=datetime.utcnow().isoformat()
        )

    # Convert conversation history to format expected by LLM
    llm_conversation_history = None
    if conversation_history:
        llm_conversation_history = [
            ConversationMessage(role=msg.role, content=msg.content, timestamp=msg.timestamp)
            for msg in conversation_history
        ]

    # Check for direct topic selection by keyword
    message_lower = message.lower()

    # Check for greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
        # Use enhanced greeting with user's name if available
        greeting = "Hello"
        if user_context and user_context.user_id:
            # In a real implementation, we would fetch the user's name
            greeting += "! Welcome back to CarfganoBot"
        else:
            greeting += "! I'm CarfganoBot from Carfgano Enterprises"
            
        response = f"{greeting}, here to help you learn about investing. What topic would you like to explore today?"
        
        # Use enhanced topics list if available
        topics_list = ENHANCED_MAIN_TOPICS_LIST if user_context else MAIN_TOPICS_LIST
        
        return ChatResponse(
            message=response,
            disclaimer=ENHANCED_DISCLAIMER if user_context else DISCLAIMER,
            suggested_topics=topics_list
        )

    # Check for direct topic matches in enhanced topics first
    if user_context:
        for topic_id, topic in ENHANCED_INVESTING_TOPICS.items():
            topic_keywords = [topic['title'].lower()] + [word.lower() for word in topic_id.split('_')]
            if any(keyword in message_lower for keyword in topic_keywords):
                return get_enhanced_topic_content(topic_id, user_context.proficiency_level)
    
    # Fall back to regular topics if no enhanced match or no user context
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
            
            # Create enhanced LLM request with user context if available
            llm_request = LLMRequest(
                prompt=prompt,
                conversation_history=llm_conversation_history,
                user_context=user_context,
                include_follow_up_questions=True
            )
            
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

            suggested_topics = [{"id": parent_id,
                                 "title": f"Back to {parent_topic}"}] if parent_id else []
            suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
            
            # Add follow-up questions as suggested topics if available
            if llm_response.follow_up_questions:
                for i, question in enumerate(llm_response.follow_up_questions):
                    suggested_topics.append({
                        "id": f"follow_up_{i}",
                        "title": question,
                        "is_question": True
                    })

            return ChatResponse(
                message=llm_response.text,
                disclaimer=ENHANCED_DISCLAIMER if user_context else DISCLAIMER,
                suggested_topics=suggested_topics,
                educational_links=llm_response.educational_links
            )

    # For open-ended questions, use the enhanced LLM with user context
    llm_request = LLMRequest(
        prompt=message,
        conversation_history=llm_conversation_history,
        user_context=user_context,
        include_follow_up_questions=True
    )
    
    llm_response = generate_response(llm_request)

    # Use suggested topics from LLM response if available, otherwise determine them
    if llm_response.suggested_topics:
        suggested_topics = llm_response.suggested_topics
        # Always add main menu option
        suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
    else:
        suggested_topics = determine_suggested_topics(message_lower, llm_response.text.lower())
    
    # Add follow-up questions as suggested topics if available
    if llm_response.follow_up_questions:
        for i, question in enumerate(llm_response.follow_up_questions):
            suggested_topics.append({
                "id": f"follow_up_{i}",
                "title": question,
                "is_question": True
            })

    return ChatResponse(
        message=llm_response.text,
        disclaimer=ENHANCED_DISCLAIMER if user_context else DISCLAIMER,
        suggested_topics=suggested_topics,
        educational_links=llm_response.educational_links
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
