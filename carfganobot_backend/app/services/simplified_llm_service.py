"""
Simplified service for handling LLM interactions with OpenAI API integration.
"""
from app.models.llm import LLMRequest, LLMResponse, UserProficiencyLevel, ConversationMessage, UserContext
from typing import List, Dict, Optional
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# Log OpenAI client initialization status
if client:
    logger.info("OpenAI client initialized successfully")
else:
    logger.warning("OpenAI client initialization failed - API key may be missing")

def generate_response(request: LLMRequest) -> LLMResponse:
    """
    Generate a response to a user prompt using OpenAI API.
    Falls back to a basic response if API is unavailable.
    """
    prompt = request.prompt
    logger.info(f"Generating response for prompt: {prompt[:50]}...")
    logger.info(f"User context: {request.user_context}")
    logger.info(f"Conversation history length: {len(request.conversation_history) if request.conversation_history else 0}")
    proficiency_level = request.user_context.proficiency_level if request.user_context else UserProficiencyLevel.BEGINNER
    
    # Default response and follow-up questions (fallback)
    default_response = (
        "I'm CarfganoBot from Carfgano Enterprises. I'm here to help you learn about investing. "
        "What topic would you like to explore today?"
    )
    
    default_follow_ups = [
        "What is investing?",
        "How do stocks work?",
        "What is diversification?"
    ]
    
    # Try to use OpenAI API if available
    if client:
        try:
            # Create system message with CarfganoBot persona
            system_message = (
                "You are CarfganoBot, an educational chatbot from Carfgano Enterprises that teaches users about investing. "
                "You have a friendly, approachable, and professional tone. "
                "Always introduce yourself as 'CarfganoBot from Carfgano Enterprises' in your first message to a user. "
                "Provide educational content about investing that is accurate and helpful. "
                f"Adapt your explanations to a {proficiency_level.value.lower()} level. "
                "Remember that you are providing educational content only, not financial advice. "
                "Keep responses concise but informative, around 2-3 paragraphs. "
                "Be dynamic and conversational in your responses, avoiding repetitive or scripted-sounding answers. "
                "Respond directly to the user's questions with relevant information rather than generic responses. "
                "Use examples and analogies to make complex investing concepts easier to understand."
            )
            
            # Create conversation history
            messages = [{"role": "system", "content": system_message}]
            
            # Add conversation history if available
            if request.conversation_history:
                for msg in request.conversation_history:
                    role = "assistant" if msg.role == "assistant" else "user"
                    messages.append({"role": role, "content": msg.content})
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            # Generate response using OpenAI API
            logger.info(f"Calling OpenAI API with {len(messages)} messages")
            logger.info(f"Using model: gpt-3.5-turbo, temperature: 0.7, max_tokens: 500")
            
            start_time = datetime.now()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            end_time = datetime.now()
            
            # Log API response time
            api_response_time = (end_time - start_time).total_seconds()
            logger.info(f"OpenAI API response time: {api_response_time:.2f} seconds")
            
            # Extract response text
            response_text = response.choices[0].message.content
            logger.info(f"Received response from OpenAI API: {response_text[:50]}...")
            logger.info(f"Response length: {len(response_text)} characters")
            
            # Generate follow-up questions
            logger.info("Generating follow-up questions...")
            follow_up_prompt = (
                "Based on the conversation so far, generate 3 follow-up questions that the user might want to ask about investing. "
                "Return only the questions as a numbered list, with no additional text."
            )
            
            follow_up_messages = messages.copy()
            follow_up_messages.append({"role": "assistant", "content": response_text})
            follow_up_messages.append({"role": "user", "content": follow_up_prompt})
            
            logger.info(f"Calling OpenAI API for follow-up questions with {len(follow_up_messages)} messages")
            follow_up_start_time = datetime.now()
            follow_up_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=follow_up_messages,
                temperature=0.7,
                max_tokens=200
            )
            follow_up_end_time = datetime.now()
            follow_up_api_time = (follow_up_end_time - follow_up_start_time).total_seconds()
            logger.info(f"Follow-up questions API response time: {follow_up_api_time:.2f} seconds")
            
            # Parse follow-up questions
            follow_up_text = follow_up_response.choices[0].message.content
            follow_up_questions = []
            
            # Extract questions from the numbered list
            for line in follow_up_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line[0] == '-'):
                    # Remove the number/bullet and any trailing/leading whitespace
                    question = line.split('.', 1)[-1].split(')', 1)[-1].strip()
                    if question:
                        follow_up_questions.append(question)
            
            # Ensure we have at least some follow-up questions
            if not follow_up_questions or len(follow_up_questions) < 3:
                follow_up_questions = default_follow_ups
            
            return LLMResponse(
                text=response_text,
                follow_up_questions=follow_up_questions[:3]  # Limit to 3 questions
            )
            
        except Exception as e:
            logger.error(f"Error using OpenAI API: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            logger.error(f"Falling back to default response")
            # Log the stack trace for debugging
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
            # Fall back to default response
    
    # Return default response if OpenAI API is unavailable or fails
    return LLMResponse(
        text=default_response,
        follow_up_questions=default_follow_ups
    )
