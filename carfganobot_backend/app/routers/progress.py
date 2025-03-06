from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.db.models import User, UserProgress, UserBadge
from app.auth.security import get_current_active_user
from app.data.investing_topics import MAIN_TOPICS_LIST, SUBTOPICS

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.post("/track/{topic_id}")
async def track_topic_progress(
    topic_id: str,
    completed: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Track user progress for a topic."""
    # Validate topic_id
    valid_topic = False
    for topic in MAIN_TOPICS_LIST:
        if topic["id"] == topic_id:
            valid_topic = True
            break
    
    if not valid_topic and topic_id in SUBTOPICS:
        valid_topic = True
    
    if not valid_topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} not found"
        )
    
    # Check if progress already exists
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.topic_id == topic_id
    ).first()
    
    if progress:
        # Update existing progress
        progress.completed = completed
        db.commit()
        db.refresh(progress)
    else:
        # Create new progress
        progress = UserProgress(
            user_id=current_user.id,
            topic_id=topic_id,
            completed=completed
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    # Check for badges
    await check_and_award_badges(current_user.id, db)
    
    return progress

@router.get("/summary")
async def get_progress_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a summary of user progress."""
    # Get all progress
    progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    
    # Count completed topics
    completed_count = sum(1 for p in progress if p.completed)
    total_topics = len(MAIN_TOPICS_LIST) + len(SUBTOPICS)
    
    # Get badges
    badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
    
    return {
        "total_topics_viewed": len(progress),
        "total_topics_completed": completed_count,
        "total_topics_available": total_topics,
        "completion_percentage": round(completed_count / total_topics * 100, 2) if total_topics > 0 else 0,
        "badges_earned": len(badges)
    }

async def check_and_award_badges(user_id: int, db: Session):
    """Check and award badges based on user progress."""
    # Get all progress
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    
    # Count completed topics
    completed_count = sum(1 for p in progress if p.completed)
    
    # Define badge criteria
    badges = [
        {"id": "first_topic", "name": "First Steps", "criteria": lambda p: len(p) >= 1},
        {"id": "five_topics", "name": "Explorer", "criteria": lambda p: len(p) >= 5},
        {"id": "first_completion", "name": "Achiever", "criteria": lambda p: completed_count >= 1},
        {"id": "five_completions", "name": "Master", "criteria": lambda p: completed_count >= 5},
    ]
    
    # Check each badge
    for badge in badges:
        if badge["criteria"](progress):
            # Check if badge already awarded
            existing_badge = db.query(UserBadge).filter(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge["id"]
            ).first()
            
            if not existing_badge:
                # Award new badge
                new_badge = UserBadge(
                    user_id=user_id,
                    badge_id=badge["id"]
                )
                db.add(new_badge)
                db.commit()
