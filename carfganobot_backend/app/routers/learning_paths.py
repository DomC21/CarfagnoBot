"""
Router for personalized learning paths based on user proficiency and progress.
"""
from fastapi import APIRouter, HTTPException, Depends
from app.auth.security import get_current_user
from app.services.proficiency_service import (
    determine_user_proficiency,
    get_recommended_learning_path
)
from app.db.database import get_db
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/learning-paths", tags=["learning-paths"])


@router.get("/recommended")
async def get_personalized_learning_path(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a personalized learning path for the authenticated user based on their proficiency level.
    """
    try:
        user_id = current_user.get("id")
        
        # Determine user proficiency level
        proficiency_level = determine_user_proficiency(db, user_id)
        
        # Get recommended learning path
        learning_path = get_recommended_learning_path(db, user_id, proficiency_level)
        
        return {
            "user_id": user_id,
            "proficiency_level": proficiency_level.value,
            "learning_path": learning_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")


@router.get("/progress")
async def get_learning_progress(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the user's learning progress, including completed topics and quiz scores.
    """
    try:
        from app.services.proficiency_service import get_completed_topics, get_user_quiz_scores
        
        user_id = current_user.get("id")
        
        # Get completed topics
        completed_topics = get_completed_topics(db, user_id)
        
        # Get quiz scores
        quiz_scores = get_user_quiz_scores(db, user_id)
        
        # Calculate overall progress
        from app.data.investing_topics import INVESTING_TOPICS, SUBTOPICS_CONTENT
        total_topics = len(INVESTING_TOPICS) + len(SUBTOPICS_CONTENT)
        completed_count = len(completed_topics)
        
        # Calculate average quiz score
        avg_score = sum(quiz_scores.values()) / len(quiz_scores) if quiz_scores else 0
        
        return {
            "user_id": user_id,
            "completed_topics": completed_topics,
            "completed_count": completed_count,
            "total_topics": total_topics,
            "progress_percentage": round(completed_count / total_topics * 100, 2) if total_topics > 0 else 0,
            "quiz_scores": quiz_scores,
            "average_quiz_score": round(avg_score, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving learning progress: {str(e)}")


@router.post("/mark-completed/{topic_id}")
async def mark_topic_completed(
    topic_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a topic as completed for the authenticated user.
    """
    try:
        from app.services.chat_service import track_user_topic_progress
        
        user_id = current_user.get("id")
        
        # Mark topic as completed
        track_user_topic_progress(user_id, topic_id, completed=True)
        
        return {"status": "success", "message": f"Topic {topic_id} marked as completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking topic as completed: {str(e)}")
