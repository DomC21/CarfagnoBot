"""
Service for handling LLM interactions.
This is a simplified mock implementation that would be replaced with actual LLM API calls.
"""
from app.models.llm import LLMRequest, LLMResponse
from app.data.investing_topics import INVESTING_TOPICS, SUBTOPICS_CONTENT, MAIN_TOPICS_LIST
import re

# Mock LLM implementation
def generate_response(request: LLMRequest) -> LLMResponse:
    """
    Generate a response using a mock LLM.
    In a production environment, this would call an actual LLM API.
    """
    prompt = request.prompt.lower()
    
    # Check if the prompt is about investing
    investing_related = is_investing_related(prompt)
    
    if not investing_related:
        return LLMResponse(
            text="I'm CarfganoBot from Carfgano Enterprises, and I'm here to help you learn about investing. "
                 "I don't have information about topics outside of investing. "
                 "Would you like to learn about investing basics, stocks, bonds, or another investing topic?",
            tokens_used=50,
            finish_reason="stop"
        )
    
    # Check if the prompt is asking for financial advice
    if is_asking_for_advice(prompt):
        return LLMResponse(
            text="I'm CarfganoBot from Carfgano Enterprises, and I'm designed to provide educational information about investing. "
                 "However, I cannot provide personalized financial advice. For personalized recommendations, "
                 "please consult with a qualified financial advisor who can consider your specific situation and goals.",
            tokens_used=60,
            finish_reason="stop"
        )
    
    # Generate a response based on the prompt
    response_text = generate_investing_response(prompt)
    
    return LLMResponse(
        text=response_text,
        tokens_used=len(response_text.split()) // 2,  # Rough estimate of tokens
        finish_reason="stop"
    )

def is_investing_related(prompt: str) -> bool:
    """
    Determine if the prompt is related to investing.
    """
    investing_keywords = [
        "invest", "stock", "bond", "etf", "mutual fund", "portfolio", "market", 
        "dividend", "equity", "asset", "security", "trading", "trader", "finance", 
        "financial", "money", "capital", "return", "risk", "diversif", "allocation",
        "retirement", "401k", "ira", "roth", "index", "fund", "yield", "interest",
        "compound", "growth", "value", "analysis", "technical", "fundamental"
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
        r"what would you (recommend|suggest)"
    ]
    
    return any(re.search(pattern, prompt) for pattern in advice_patterns)

def generate_investing_response(prompt: str) -> str:
    """
    Generate a response about investing based on the prompt.
    This is a simplified implementation that would be replaced with actual LLM responses.
    """
    # Check for specific topics
    for topic_id, topic_data in INVESTING_TOPICS.items():
        topic_keywords = [topic_data['title'].lower()] + [word.lower() for word in topic_id.split('_')]
        
        if any(keyword in prompt for keyword in topic_keywords):
            return f"I'm CarfganoBot from Carfgano Enterprises. {topic_data['content'].strip()}"
    
    # Check for subtopics
    for subtopic_id, content in SUBTOPICS_CONTENT.items():
        subtopic_keywords = [subtopic_id.replace('_', ' ').lower()]
        
        # Find the subtopic title
        for topic in INVESTING_TOPICS.values():
            for subtopic in topic.get('subtopics', []):
                if subtopic['id'] == subtopic_id:
                    subtopic_keywords.append(subtopic['title'].lower())
        
        if any(keyword in prompt for keyword in subtopic_keywords):
            return f"I'm CarfganoBot from Carfgano Enterprises. {content.strip()}"
    
    # General investing questions
    if "what is investing" in prompt or "how to start investing" in prompt:
        return ("I'm CarfganoBot from Carfgano Enterprises. Investing is the process of allocating resources, usually money, "
                "with the expectation of generating income or profit over time. To start investing, you should first "
                "establish your financial goals, create an emergency fund, pay off high-interest debt, understand "
                "your risk tolerance, and then choose appropriate investment vehicles like stocks, bonds, mutual funds, "
                "or ETFs based on your goals and risk tolerance.")
    
    if "diversify" in prompt or "diversification" in prompt:
        return ("I'm CarfganoBot from Carfgano Enterprises. Diversification is a risk management strategy that involves "
                "spreading your investments across various financial instruments, industries, and other categories. "
                "It aims to maximize returns by investing in different areas that would each react differently to the "
                "same event. A well-diversified portfolio might include stocks, bonds, real estate, and perhaps other "
                "investments like commodities or international securities.")
    
    if "risk" in prompt:
        return ("I'm CarfganoBot from Carfgano Enterprises. In investing, risk refers to the possibility of losing some or all "
                "of an investment. Generally, higher risk investments have the potential for higher returns, while lower "
                "risk investments typically offer lower returns. Common types of investment risk include market risk, "
                "inflation risk, liquidity risk, and concentration risk. Risk management strategies include diversification, "
                "asset allocation, and position sizing.")
    
    # Default response for general investing questions
    return ("I'm CarfganoBot from Carfgano Enterprises, here to help you learn about investing. "
            "I can provide information on various investing topics like stocks, bonds, mutual funds, "
            "ETFs, risk management, and market analysis. What specific aspect of investing would you like to learn about?")
