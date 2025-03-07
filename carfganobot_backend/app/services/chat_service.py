"""
Service for handling chat functionality and topic navigation with enhanced AI coaching capabilities.
"""
from app.models.chat import ChatRequest, ChatResponse
from app.models.llm import LLMRequest, ConversationMessage, UserContext, UserProficiencyLevel
from app.data.investing_topics import INVESTING_TOPICS, SUBTOPICS_CONTENT, MAIN_TOPICS_LIST, DISCLAIMER
from app.data.enhanced_investing_topics import ENHANCED_INVESTING_TOPICS, ENHANCED_MAIN_TOPICS_LIST, ENHANCED_DISCLAIMER
from app.services.simplified_llm_service import generate_response
from app.services.proficiency_service import (
    determine_user_proficiency as get_proficiency,
    get_completed_topics as get_topics,
    get_user_quiz_scores as get_quiz_scores,
    get_user_interests as get_interests,
    track_topic_progress
)
from app.db.database import get_db
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
    Uses the proficiency service to query the database for the user's quiz results and topic progress.
    """
    try:
        # Get database session
        db = next(get_db())
        
        # Use proficiency service to determine user proficiency
        proficiency_level = get_proficiency(db, user_id)
        
        return proficiency_level
    except Exception as e:
        # Log the error in a real implementation
        print(f"Error determining user proficiency: {e}")
        # Fall back to beginner level
        return UserProficiencyLevel.BEGINNER
    finally:
        # Close database session
        if 'db' in locals():
            db.close()


def get_completed_topics(user_id: int) -> List[str]:
    """
    Get the list of topics that the user has completed.
    Uses the proficiency service to query the database for the user's topic progress.
    """
    try:
        # Get database session
        db = next(get_db())
        
        # Use proficiency service to get completed topics
        completed_topics = get_topics(db, user_id)
        
        return completed_topics
    except Exception as e:
        # Log the error in a real implementation
        print(f"Error getting completed topics: {e}")
        # Return empty list as fallback
        return []
    finally:
        # Close database session
        if 'db' in locals():
            db.close()


def get_user_quiz_scores(user_id: int) -> Dict[str, float]:
    """
    Get the user's quiz scores for different topics.
    Uses the proficiency service to query the database for the user's quiz results.
    """
    try:
        # Get database session
        db = next(get_db())
        
        # Use proficiency service to get quiz scores
        quiz_scores = get_quiz_scores(db, user_id)
        
        return quiz_scores
    except Exception as e:
        # Log the error in a real implementation
        print(f"Error getting user quiz scores: {e}")
        # Return empty dict as fallback
        return {}
    finally:
        # Close database session
        if 'db' in locals():
            db.close()


def get_user_interests(user_id: int) -> List[str]:
    """
    Get the user's interests based on their interactions with the app.
    Uses the proficiency service to analyze the user's behavior and quiz results.
    """
    try:
        # Get database session
        db = next(get_db())
        
        # Use proficiency service to get user interests
        interests = get_interests(db, user_id)
        
        return interests
    except Exception as e:
        # Log the error in a real implementation
        print(f"Error getting user interests: {e}")
        # Return empty list as fallback
        return []
    finally:
        # Close database session
        if 'db' in locals():
            db.close()


def track_user_topic_progress(user_id: int, topic_id: str, completed: bool = False) -> None:
    """
    Track a user's progress on a topic.
    Uses the proficiency service to update the database with the user's topic progress.
    """
    try:
        # Get database session
        db = next(get_db())
        
        # Use proficiency service to track topic progress
        track_topic_progress(db, user_id, topic_id, completed)
    except Exception as e:
        # Log the error in a real implementation
        print(f"Error tracking topic progress: {e}")
    finally:
        # Close database session
        if 'db' in locals():
            db.close()


def process_chat_message(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message from the user and return a response.
    Uses the enhanced LLM service to generate personalized responses based on user context.
    Also tracks user topic progress for authenticated users.
    """
    message = request.message
    conversation_history = request.conversation_history
    user_id = request.user_id
    selected_topic = request.selected_topic
    
    # Create user context if user is authenticated
    user_context = None
    if user_id:
        # Get user data from the database
        user_context = UserContext(
            user_id=user_id,
            proficiency_level=determine_user_proficiency(user_id),
            topics_completed=get_completed_topics(user_id),
            quiz_scores=get_user_quiz_scores(user_id),
            interests=get_user_interests(user_id),
            last_interaction=datetime.utcnow().isoformat()
        )
        
        # Track topic progress if a topic was selected
        if selected_topic:
            track_user_topic_progress(user_id, selected_topic)

    # Convert conversation history to format expected by LLM
    llm_conversation_history = None
    if conversation_history:
        llm_conversation_history = [
            ConversationMessage(text=msg.content, is_bot=msg.role == "assistant", timestamp=msg.timestamp)
            for msg in conversation_history
        ]

    # Check for direct topic selection by keyword
    message_lower = message.lower()

    # For main menu request, return the topic list with AI-generated greeting
    # This is kept as a special case to provide structured navigation
    if message_lower in ["menu", "topics", "main menu", "show topics", "show menu"]:
        # Use the OpenAI API to generate a personalized greeting
        menu_prompt = "Generate a friendly welcome message for an investing education chatbot called CarfganoBot. The message should invite the user to explore investing topics. Keep it under 2 sentences."
        
        # Create LLM request for menu greeting
        menu_llm_request = LLMRequest(
            prompt=menu_prompt,
            user_context=user_context,
            include_follow_up_questions=False
        )
        
        # Generate personalized menu greeting
        menu_response = generate_response(menu_llm_request)
        
        # Add the topic selection prompt
        message_text = f"{menu_response.text}\n\nPlease select a topic you'd like to explore:"
        
        # Use enhanced topics list if available
        topics_list = ENHANCED_MAIN_TOPICS_LIST if user_context else MAIN_TOPICS_LIST
        
        return ChatResponse(
            message=message_text,
            disclaimer=ENHANCED_DISCLAIMER if user_context else DISCLAIMER,
            suggested_topics=topics_list
        )

    # For all other messages, use the OpenAI API to generate a dynamic response
    # Create enhanced LLM request with user context if available
    llm_request = LLMRequest(
        prompt=message,
        conversation_history=llm_conversation_history,
        user_context=user_context,
        include_follow_up_questions=True
    )
    
    # Generate response using OpenAI API
    llm_response = generate_response(llm_request)
    
    # Determine suggested topics based on the response
    suggested_topics = determine_suggested_topics(message_lower, llm_response.text.lower())
    
    # Add follow-up questions as suggested topics if available
    if llm_response.follow_up_questions:
        for i, question in enumerate(llm_response.follow_up_questions):
            suggested_topics.append({
                "id": f"follow_up_{i}",
                "title": question,
                "is_question": True
            })
    
    # Always add main menu option
    suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})
    
    return ChatResponse(
        message=llm_response.text,
        disclaimer=ENHANCED_DISCLAIMER if user_context else DISCLAIMER,
        suggested_topics=suggested_topics,
        educational_links=llm_response.educational_links
    )


def determine_suggested_topics(user_message: str, response_text: str) -> List[Dict[str, str]]:
    """
    Determine relevant suggested topics based on the user message and response.
    Uses keyword matching with weighted scoring to suggest the most relevant topics.
    """
    suggested_topics = []

    # Enhanced topic keywords with more comprehensive coverage
    topic_keywords = {
        "investing_basics": ["basic", "beginner", "start", "new to investing", "fundamental", "introduction", 
                            "getting started", "learn", "education", "first step", "foundation", "principle"],
        "stocks": ["stock", "share", "equity", "dividend", "shareholder", "market cap", "ipo", "earnings", 
                  "p/e ratio", "growth stock", "value stock", "blue chip", "nasdaq", "nyse"],
        "bonds": ["bond", "fixed income", "debt", "yield", "coupon", "interest rate", "treasury", "corporate bond", 
                 "municipal", "maturity", "duration", "credit rating", "junk bond", "investment grade"],
        "risk_management": ["risk", "diversif", "portfolio", "allocation", "asset class", "rebalance", "hedge", 
                           "volatility", "downside", "protection", "insurance", "correlation", "beta", "standard deviation"],
        "market_analysis": ["analysis", "technical", "fundamental", "chart", "indicator", "pattern", "trend", 
                           "moving average", "resistance", "support", "volume", "momentum", "oscillator", "candlestick"],
        "advanced_concepts": ["advanced", "option", "future", "derivative", "alternative", "leverage", "margin", 
                             "short selling", "arbitrage", "forex", "commodity", "hedge fund", "private equity", "reit"]
    }

    # Count keyword matches for each topic
    topic_scores = {topic_id: 0 for topic_id in topic_keywords.keys()}

    # Process user message and response text for better matching
    user_message_lower = user_message.lower()
    response_text_lower = response_text.lower()

    for topic_id, keywords in topic_keywords.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Check for exact matches or word boundary matches to avoid partial word matches
            if f" {keyword_lower} " in f" {user_message_lower} " or user_message_lower.startswith(f"{keyword_lower} ") or user_message_lower.endswith(f" {keyword_lower}"):
                topic_scores[topic_id] += 2  # Higher weight for user message
            if f" {keyword_lower} " in f" {response_text_lower} " or response_text_lower.startswith(f"{keyword_lower} ") or response_text_lower.endswith(f" {keyword_lower}"):
                topic_scores[topic_id] += 1  # Lower weight for response text

    # Get top 3 topics
    top_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)[:3]

    # Add suggested topics if they have a score > 0
    for topic_id, score in top_topics:
        if score > 0:
            # Use enhanced topics if available, otherwise fall back to regular topics
            if topic_id in ENHANCED_INVESTING_TOPICS:
                topic = ENHANCED_INVESTING_TOPICS[topic_id]
            else:
                topic = INVESTING_TOPICS[topic_id]
            suggested_topics.append({"id": topic_id, "title": topic["title"]})

    # If no topics matched, suggest investing basics as a fallback
    if not suggested_topics:
        if "investing_basics" in ENHANCED_INVESTING_TOPICS:
            topic = ENHANCED_INVESTING_TOPICS["investing_basics"]
        else:
            topic = INVESTING_TOPICS["investing_basics"]
        suggested_topics.append({"id": "investing_basics", "title": topic["title"]})

    # Always add main menu option
    suggested_topics.append({"id": "main_menu", "title": "Back to Main Topics"})

    return suggested_topics
