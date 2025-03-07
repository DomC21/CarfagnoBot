"""
Service for handling LLM interactions with enhanced AI coaching capabilities.
This implementation provides personalized responses based on user proficiency and context.
"""
from app.models.llm import (
    LLMRequest, LLMResponse, UserProficiencyLevel,
    ConversationMessage, UserContext
)
from app.data.investing_topics import INVESTING_TOPICS, SUBTOPICS_CONTENT
from app.data.enhanced_investing_topics import (
    ENHANCED_INVESTING_TOPICS, ENHANCED_SUBTOPICS_CONTENT,
    EDUCATIONAL_RESOURCES, ENHANCED_DISCLAIMER, ENHANCED_MAIN_TOPICS_LIST
)
import re
import random
import os
import openai
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY", "")



def generate_response(request: LLMRequest) -> LLMResponse:
    """
    Generate an enhanced response using the OpenAI API and AI coach capabilities.
    Provides personalized content based on user proficiency and conversation history.
    """
    prompt = request.prompt.lower()
    
    # Get user proficiency level
    proficiency_level = UserProficiencyLevel.BEGINNER
    if request.user_context:
        proficiency_level = request.user_context.proficiency_level or UserProficiencyLevel.BEGINNER
    
    # Check if the prompt is about investing
    investing_related = is_investing_related(prompt)

    if not investing_related:
        return LLMResponse(
            text="I'm CarfganoBot from Carfgano Enterprises, and I'm here to help you learn about investing. "
            "I don't have information about topics outside of investing. "
            "Would you like to learn about investing basics, stocks, bonds, or another investing topic?",
            follow_up_questions=get_general_follow_up_questions(),
            tokens_used=50,
            finish_reason="stop"
        )

    # Check if the prompt is asking for financial advice
    if is_asking_for_advice(prompt):
        return LLMResponse(
            text="I'm CarfganoBot from Carfgano Enterprises, and I'm designed to provide educational information about investing. "
            "However, I cannot provide personalized financial advice. For personalized recommendations, "
            "please consult with a qualified financial advisor who can consider your specific situation and goals.",
            follow_up_questions=get_general_follow_up_questions(),
            tokens_used=60,
            finish_reason="stop"
        )

    # Check if OpenAI API key is available
    if openai.api_key:
        # Use OpenAI API for enhanced responses
        return generate_openai_response(
            prompt=prompt,
            proficiency_level=proficiency_level,
            conversation_history=request.conversation_history,
            user_context=request.user_context,
            include_follow_up=request.include_follow_up_questions
        )
    else:
        # Fallback to local response generation
        response = generate_enhanced_response(
            prompt=prompt,
            proficiency_level=proficiency_level,
            conversation_history=request.conversation_history,
            user_context=request.user_context,
            include_follow_up=request.include_follow_up_questions
        )
        return response


def is_investing_related(prompt: str) -> bool:
    """
    Determine if the prompt is related to investing.
    """
    investing_keywords = [
        "invest", "stock", "bond", "etf", "mutual fund", "portfolio", "market",
        "dividend", "equity", "asset", "security", "trading", "trader", "finance",
        "financial", "money", "capital", "return", "risk", "diversif", "allocation",
        "retirement", "401k", "ira", "roth", "index", "fund", "yield", "interest",
        "compound", "growth", "value", "analysis", "technical", "fundamental",
        "inflation", "recession", "bull market", "bear market", "volatility",
        "liquidity", "asset class", "sector", "industry", "valuation", "earnings"
    ]

    return any(keyword in prompt for keyword in investing_keywords)


def is_asking_for_advice(prompt: str) -> bool:
    """
    Determine if the prompt is asking for personalized financial advice.
    """
    advice_patterns = [
        r"should i (buy|sell|invest in)",
        r"what (stocks|bonds|etfs|funds) should i",
        r"is it a good time to",
        r"recommend (a|some|any)",
        r"my portfolio",
        r"my investments",
        r"for me",
        r"my (financial|money|retirement)",
        r"i have \$[0-9,]+",
        r"advice (for|on)",
        r"what would you (recommend|suggest)",
        r"how much should i",
        r"when should i",
        r"is this a good",
        r"what do you think of"
    ]

    return any(re.search(pattern, prompt) for pattern in advice_patterns)


def generate_enhanced_response(
    prompt: str,
    proficiency_level: UserProficiencyLevel,
    conversation_history: Optional[List[ConversationMessage]] = None,
    user_context: Optional[UserContext] = None,
    include_follow_up: bool = True
) -> LLMResponse:
    """
    Generate an enhanced response about investing based on the prompt and user context.
    Provides personalized content based on user proficiency level and conversation history.
    """
    # Default values
    response_text = ""
    follow_up_questions = []
    suggested_topics = []
    educational_links = []
    
    # Convert proficiency level to string for content lookup
    prof_level = proficiency_level.value
    
    # Check for specific topics in enhanced content
    for topic_id, topic_data in ENHANCED_INVESTING_TOPICS.items():
        topic_keywords = [topic_data['title'].lower()] + [word.lower() for word in topic_id.split('_')]
        
        if any(keyword in prompt for keyword in topic_keywords):
            # Get content for appropriate proficiency level
            if prof_level in topic_data['content']:
                content = topic_data['content'][prof_level]
            else:
                # Fallback to beginner if specific level not available
                content = topic_data['content'].get('beginner', topic_data['content'].get(list(topic_data['content'].keys())[0]))
            
            response_text = f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
            
            # Add follow-up questions if available and requested
            if include_follow_up and 'follow_up_questions' in topic_data:
                follow_up_questions = random.sample(
                    topic_data['follow_up_questions'],
                    min(3, len(topic_data['follow_up_questions']))
                )
            
            # Add educational links if available
            if 'educational_links' in topic_data:
                educational_links = [
                    link for link in topic_data['educational_links']
                    if link.get('difficulty', 'beginner') == prof_level or not link.get('difficulty')
                ]
                
                # If no links match the proficiency level, include beginner links
                if not educational_links and prof_level != 'beginner':
                    educational_links = [
                        link for link in topic_data['educational_links']
                        if link.get('difficulty', 'beginner') == 'beginner'
                    ]
            
            # Add suggested topics based on subtopics
            if 'subtopics' in topic_data:
                suggested_topics = [
                    {"id": subtopic['id'], "title": subtopic['title']}
                    for subtopic in topic_data['subtopics'][:3]
                ]
            
            break
    
    # If no topic match, check for subtopics in enhanced content
    if not response_text:
        for subtopic_id, content_by_level in ENHANCED_SUBTOPICS_CONTENT.items():
            subtopic_keywords = [subtopic_id.replace('_', ' ').lower()]
            
            # Find the subtopic title
            for topic in ENHANCED_INVESTING_TOPICS.values():
                for subtopic in topic.get('subtopics', []):
                    if subtopic['id'] == subtopic_id:
                        subtopic_keywords.append(subtopic['title'].lower())
            
            if any(keyword in prompt for keyword in subtopic_keywords):
                # Get content for appropriate proficiency level
                if prof_level in content_by_level:
                    content = content_by_level[prof_level]
                else:
                    # Fallback to beginner if specific level not available
                    content = content_by_level.get('beginner', content_by_level.get(list(content_by_level.keys())[0]))
                
                response_text = f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
                
                # Find parent topic for suggested topics and educational links
                parent_topic_id = None
                for topic_id, topic_data in ENHANCED_INVESTING_TOPICS.items():
                    for subtopic in topic_data.get('subtopics', []):
                        if subtopic['id'] == subtopic_id:
                            parent_topic_id = topic_id
                            break
                    if parent_topic_id:
                        break
                
                # Add educational links from parent topic if available
                if parent_topic_id and parent_topic_id in EDUCATIONAL_RESOURCES:
                    educational_links = [
                        {
                            "title": resource["title"],
                            "description": resource["description"],
                            "url": resource["url"]
                        }
                        for resource in EDUCATIONAL_RESOURCES[parent_topic_id]
                        if resource.get('difficulty', 'beginner') == prof_level or not resource.get('difficulty')
                    ]
                
                # Add suggested topics from parent topic
                if parent_topic_id and parent_topic_id in ENHANCED_INVESTING_TOPICS:
                    parent_topic = ENHANCED_INVESTING_TOPICS[parent_topic_id]
                    suggested_topics = [
                        {"id": subtopic['id'], "title": subtopic['title']}
                        for subtopic in parent_topic.get('subtopics', [])
                        if subtopic['id'] != subtopic_id
                    ][:3]
                
                break
    
    # If still no match, check original content
    if not response_text:
        # Check for specific topics in original content
        for topic_id, topic_data in INVESTING_TOPICS.items():
            topic_keywords = [topic_data['title'].lower()] + [word.lower() for word in topic_id.split('_')]
            
            if any(keyword in prompt for keyword in topic_keywords):
                response_text = f"I'm CarfganoBot from Carfgano Enterprises. {topic_data['content'].strip()}"
                
                # Add suggested topics based on subtopics
                if 'subtopics' in topic_data:
                    suggested_topics = [
                        {"id": subtopic['id'], "title": subtopic['title']}
                        for subtopic in topic_data['subtopics'][:3]
                    ]
                
                break
        
        # Check for subtopics in original content
        if not response_text:
            for subtopic_id, content in SUBTOPICS_CONTENT.items():
                subtopic_keywords = [subtopic_id.replace('_', ' ').lower()]
                
                # Find the subtopic title
                for topic in INVESTING_TOPICS.values():
                    for subtopic in topic.get('subtopics', []):
                        if subtopic['id'] == subtopic_id:
                            subtopic_keywords.append(subtopic['title'].lower())
                
                if any(keyword in prompt for keyword in subtopic_keywords):
                    response_text = f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
                    break
    
    # Handle general investing questions
    if not response_text:
        if "what is investing" in prompt or "how to start investing" in prompt:
            # Get content based on proficiency level
            if "investing_basics" in ENHANCED_INVESTING_TOPICS:
                content = ENHANCED_INVESTING_TOPICS["investing_basics"]["content"].get(
                    prof_level,
                    ENHANCED_INVESTING_TOPICS["investing_basics"]["content"].get("beginner")
                )
                response_text = f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
                
                # Add follow-up questions
                if include_follow_up and 'follow_up_questions' in ENHANCED_INVESTING_TOPICS["investing_basics"]:
                    follow_up_questions = random.sample(
                        ENHANCED_INVESTING_TOPICS["investing_basics"]["follow_up_questions"],
                        min(3, len(ENHANCED_INVESTING_TOPICS["investing_basics"]["follow_up_questions"]))
                    )
                
                # Add educational links
                if "investing_basics" in EDUCATIONAL_RESOURCES:
                    educational_links = [
                        {
                            "title": resource["title"],
                            "description": resource["description"],
                            "url": resource["url"]
                        }
                        for resource in EDUCATIONAL_RESOURCES["investing_basics"]
                        if resource.get('difficulty', 'beginner') == prof_level or not resource.get('difficulty')
                    ]
            else:
                response_text = (
                    "I'm CarfganoBot from Carfgano Enterprises. Investing is the process of allocating resources, usually money, "
                    "with the expectation of generating income or profit over time. To start investing, you should first "
                    "establish your financial goals, create an emergency fund, pay off high-interest debt, understand "
                    "your risk tolerance, and then choose appropriate investment vehicles like stocks, bonds, mutual funds, "
                    "or ETFs based on your goals and risk tolerance."
                )
        
        elif "diversify" in prompt or "diversification" in prompt:
            # Check if enhanced content is available
            if "diversification" in ENHANCED_SUBTOPICS_CONTENT:
                content = ENHANCED_SUBTOPICS_CONTENT["diversification"].get(
                    prof_level,
                    ENHANCED_SUBTOPICS_CONTENT["diversification"].get("beginner")
                )
                response_text = f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
            else:
                response_text = (
                    "I'm CarfganoBot from Carfgano Enterprises. Diversification is a risk management strategy that involves "
                    "spreading your investments across various financial instruments, industries, and other categories. "
                    "It aims to maximize returns by investing in different areas that would each react differently to the "
                    "same event. A well-diversified portfolio might include stocks, bonds, real estate, and perhaps other "
                    "investments like commodities or international securities."
                )
        
        elif "risk" in prompt:
            # Check if enhanced content is available
            if "risk_management" in ENHANCED_INVESTING_TOPICS:
                content = ENHANCED_INVESTING_TOPICS["risk_management"]["content"].get(
                    prof_level,
                    ENHANCED_INVESTING_TOPICS["risk_management"]["content"].get("beginner")
                )
                response_text = f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
                
                # Add follow-up questions
                if include_follow_up and 'follow_up_questions' in ENHANCED_INVESTING_TOPICS["risk_management"]:
                    follow_up_questions = random.sample(
                        ENHANCED_INVESTING_TOPICS["risk_management"]["follow_up_questions"],
                        min(3, len(ENHANCED_INVESTING_TOPICS["risk_management"]["follow_up_questions"]))
                    )
                
                # Add educational links
                if "risk_management" in EDUCATIONAL_RESOURCES:
                    educational_links = [
                        {
                            "title": resource["title"],
                            "description": resource["description"],
                            "url": resource["url"]
                        }
                        for resource in EDUCATIONAL_RESOURCES["risk_management"]
                        if resource.get('difficulty', 'beginner') == prof_level or not resource.get('difficulty')
                    ]
            else:
                response_text = (
                    "I'm CarfganoBot from Carfgano Enterprises. In investing, risk refers to the possibility of losing some or all "
                    "of an investment. Generally, higher risk investments have the potential for higher returns, while lower "
                    "risk investments typically offer lower returns. Common types of investment risk include market risk, "
                    "inflation risk, liquidity risk, and concentration risk. Risk management strategies include diversification, "
                    "asset allocation, and position sizing."
                )
    
    # Default response if no specific match found
    if not response_text:
        response_text = (
            "I'm CarfganoBot from Carfgano Enterprises, here to help you learn about investing. "
            "I can provide information on various investing topics like stocks, bonds, mutual funds, "
            "ETFs, risk management, and market analysis. What specific aspect of investing would you like to learn about?"
        )
        
        # Add general follow-up questions
        if include_follow_up:
            follow_up_questions = get_general_follow_up_questions()
        
        # Add suggested topics
        suggested_topics = [
            {"id": topic["id"], "title": topic["title"]}
            for topic in ENHANCED_MAIN_TOPICS_LIST[:3]
        ]
    
    # Add personalized greeting if user context is available
    if user_context and user_context.user_id and not response_text.startswith("I'm CarfganoBot"):
        response_text = f"I'm CarfganoBot from Carfgano Enterprises. {response_text}"
    
    # Add proficiency-based learning path suggestion
    if user_context and user_context.proficiency_level:
        if user_context.proficiency_level == UserProficiencyLevel.BEGINNER:
            if not suggested_topics:
                suggested_topics = [
                    {"id": "investing_basics", "title": "Investing Basics"},
                    {"id": "stocks", "title": "Stocks"},
                    {"id": "bonds", "title": "Bonds"}
                ]
        elif user_context.proficiency_level == UserProficiencyLevel.INTERMEDIATE:
            if not suggested_topics:
                suggested_topics = [
                    {"id": "risk_management", "title": "Risk Management"},
                    {"id": "market_analysis", "title": "Market Analysis"},
                    {"id": "diversification", "title": "Diversification"}
                ]
        elif user_context.proficiency_level == UserProficiencyLevel.ADVANCED:
            if not suggested_topics:
                suggested_topics = [
                    {"id": "advanced_concepts", "title": "Advanced Concepts"},
                    {"id": "options_trading", "title": "Options Trading"},
                    {"id": "alternative_investments", "title": "Alternative Investments"}
                ]
    
    # Create the response
    return LLMResponse(
        text=response_text,
        follow_up_questions=follow_up_questions if include_follow_up else None,
        suggested_topics=suggested_topics if suggested_topics else None,
        educational_links=educational_links if educational_links else None,
        tokens_used=len(response_text.split()) // 2,  # Rough estimate of tokens
        finish_reason="stop"
    )


def get_general_follow_up_questions() -> List[str]:
    """
    Get general follow-up questions about investing.
    """
    all_questions = [
        "What's the difference between stocks and bonds?",
        "How does compound interest work?",
        "What is diversification and why is it important?",
        "How do I determine my risk tolerance?",
        "What are the different types of investment accounts?",
        "How do market cycles affect investments?",
        "What's the difference between active and passive investing?",
        "How do taxes impact investment returns?",
        "What are ETFs and how do they differ from mutual funds?",
        "How should I think about asset allocation?"
    ]
    
    return random.sample(all_questions, 3)
