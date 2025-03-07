"""
Service for tracking and determining user proficiency levels based on quiz results and topic completions.
"""
from app.models.llm import UserProficiencyLevel
from app.db.models import User, QuizResult, UserProgress
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
import statistics
from datetime import datetime, timedelta


def determine_user_proficiency(db: Session, user_id: int) -> UserProficiencyLevel:
    """
    Determine a user's proficiency level based on their quiz results and topic completions.
    
    Algorithm:
    1. Calculate average quiz scores across all topics
    2. Count completed topics
    3. Analyze quiz completion patterns (difficulty levels attempted)
    4. Consider recency of activity
    5. Combine factors to determine overall proficiency level
    """
    # Get user's quiz results
    quiz_scores = get_user_quiz_scores(db, user_id)
    
    # Get user's completed topics
    completed_topics = get_completed_topics(db, user_id)
    
    # Get quiz difficulty distribution
    difficulty_distribution = get_quiz_difficulty_distribution(db, user_id)
    
    # Calculate proficiency score based on multiple factors
    proficiency_score = calculate_proficiency_score(
        quiz_scores=quiz_scores,
        completed_topics=completed_topics,
        difficulty_distribution=difficulty_distribution
    )
    
    # Map proficiency score to proficiency level
    return map_score_to_proficiency_level(proficiency_score)


def get_user_quiz_scores(db: Session, user_id: int) -> Dict[str, float]:
    """
    Get a user's quiz scores by topic.
    Returns a dictionary mapping topic_id to average score.
    """
    # Query all quiz results for the user
    quiz_results = (
        db.query(QuizResult)
        .filter(QuizResult.user_id == user_id)
        .all()
    )
    
    # Group scores by topic
    topic_scores = {}
    
    for result in quiz_results:
        # Get the quiz to find its topic
        quiz = result.quiz
        topic_id = quiz.topic_id
        
        if topic_id not in topic_scores:
            topic_scores[topic_id] = []
            
        topic_scores[topic_id].append(result.score)
    
    # Calculate average score for each topic
    return {
        topic_id: statistics.mean(scores) if scores else 0
        for topic_id, scores in topic_scores.items()
    }


def get_completed_topics(db: Session, user_id: int) -> List[str]:
    """
    Get a list of topics that the user has completed.
    """
    # Query completed topics for the user
    completed_progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.completed == True)
        .all()
    )
    
    return [progress.topic_id for progress in completed_progress]


def get_quiz_difficulty_distribution(db: Session, user_id: int) -> Dict[str, int]:
    """
    Get the distribution of quiz difficulties that the user has completed.
    Returns a dictionary mapping difficulty level to count.
    """
    # Query all quiz results for the user
    quiz_results = (
        db.query(QuizResult)
        .filter(QuizResult.user_id == user_id)
        .all()
    )
    
    # Count quizzes by difficulty
    difficulty_counts = {
        "beginner": 0,
        "intermediate": 0,
        "advanced": 0
    }
    
    for result in quiz_results:
        quiz = result.quiz
        difficulty = quiz.difficulty.lower()
        
        if difficulty in difficulty_counts:
            difficulty_counts[difficulty] += 1
    
    return difficulty_counts


def calculate_proficiency_score(
    quiz_scores: Dict[str, float],
    completed_topics: List[str],
    difficulty_distribution: Dict[str, int]
) -> float:
    """
    Calculate a proficiency score based on multiple factors.
    Returns a score between 0 and 100.
    """
    # Factor 1: Average quiz score (0-100)
    avg_score = statistics.mean(quiz_scores.values()) if quiz_scores else 0
    
    # Factor 2: Number of completed topics (normalized to 0-100)
    # Assume 20 topics is the maximum for normalization
    topic_score = min(len(completed_topics) / 20 * 100, 100)
    
    # Factor 3: Quiz difficulty distribution (0-100)
    # Weight advanced quizzes more heavily
    difficulty_score = (
        difficulty_distribution.get("beginner", 0) * 1 +
        difficulty_distribution.get("intermediate", 0) * 2 +
        difficulty_distribution.get("advanced", 0) * 3
    )
    # Normalize to 0-100 (assume 20 total quizzes is the maximum)
    difficulty_score = min(difficulty_score / 60 * 100, 100)
    
    # Combine factors with weights
    # 50% quiz scores, 30% topic completion, 20% difficulty distribution
    proficiency_score = (
        avg_score * 0.5 +
        topic_score * 0.3 +
        difficulty_score * 0.2
    )
    
    return proficiency_score


def map_score_to_proficiency_level(score: float) -> UserProficiencyLevel:
    """
    Map a proficiency score to a proficiency level.
    """
    if score < 40:
        return UserProficiencyLevel.BEGINNER
    elif score < 75:
        return UserProficiencyLevel.INTERMEDIATE
    else:
        return UserProficiencyLevel.ADVANCED


def track_topic_progress(db: Session, user_id: int, topic_id: str, completed: bool = False) -> UserProgress:
    """
    Track a user's progress on a topic.
    """
    # Check if progress record already exists
    progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.topic_id == topic_id)
        .first()
    )
    
    if progress:
        # Update existing record
        progress.viewed_at = datetime.utcnow()
        if completed:
            progress.completed = True
    else:
        # Create new record
        progress = UserProgress(
            user_id=user_id,
            topic_id=topic_id,
            completed=completed,
            viewed_at=datetime.utcnow()
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    
    return progress


def get_user_interests(db: Session, user_id: int) -> List[str]:
    """
    Determine a user's interests based on their quiz results and topic views.
    Returns a list of topic IDs that the user is interested in.
    """
    # Get topics the user has viewed recently
    recent_views = (
        db.query(UserProgress)
        .filter(
            UserProgress.user_id == user_id,
            UserProgress.viewed_at >= datetime.utcnow() - timedelta(days=30)
        )
        .all()
    )
    
    # Get topics the user has performed well on in quizzes
    quiz_scores = get_user_quiz_scores(db, user_id)
    high_score_topics = [topic_id for topic_id, score in quiz_scores.items() if score >= 70]
    
    # Combine and deduplicate
    interests = list(set([progress.topic_id for progress in recent_views] + high_score_topics))
    
    return interests


def get_recommended_learning_path(
    db: Session,
    user_id: int,
    proficiency_level: Optional[UserProficiencyLevel] = None
) -> List[Dict[str, str]]:
    """
    Generate a personalized learning path for the user based on their proficiency level.
    Returns a list of recommended topics in suggested order.
    """
    if proficiency_level is None:
        proficiency_level = determine_user_proficiency(db, user_id)
    
    # Get completed topics
    completed_topics = get_completed_topics(db, user_id)
    
    # Define topic progression paths based on proficiency level
    if proficiency_level == UserProficiencyLevel.BEGINNER:
        path = [
            {"id": "investing_basics", "title": "Investing Basics"},
            {"id": "stocks", "title": "Stocks"},
            {"id": "bonds", "title": "Bonds"},
            {"id": "mutual_funds", "title": "Mutual Funds"},
            {"id": "etfs", "title": "ETFs"},
            {"id": "risk_management", "title": "Risk Management"}
        ]
    elif proficiency_level == UserProficiencyLevel.INTERMEDIATE:
        path = [
            {"id": "risk_management", "title": "Risk Management"},
            {"id": "market_analysis", "title": "Market Analysis"},
            {"id": "diversification", "title": "Diversification"},
            {"id": "asset_allocation", "title": "Asset Allocation"},
            {"id": "retirement_planning", "title": "Retirement Planning"},
            {"id": "tax_strategies", "title": "Tax Strategies"}
        ]
    else:  # Advanced
        path = [
            {"id": "advanced_concepts", "title": "Advanced Concepts"},
            {"id": "options_trading", "title": "Options Trading"},
            {"id": "alternative_investments", "title": "Alternative Investments"},
            {"id": "portfolio_optimization", "title": "Portfolio Optimization"},
            {"id": "macroeconomic_analysis", "title": "Macroeconomic Analysis"},
            {"id": "quantitative_investing", "title": "Quantitative Investing"}
        ]
    
    # Filter out completed topics
    path = [topic for topic in path if topic["id"] not in completed_topics]
    
    return path
