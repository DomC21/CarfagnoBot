"""
Badges data for the CarfganoBot application.
"""

# List of available badges
BADGES = [
    {
        "id": "first_topic",
        "name": "First Steps",
        "description": "Viewed your first investing topic",
        "icon": "🏁"
    },
    {
        "id": "five_topics",
        "name": "Explorer",
        "description": "Viewed 5 different investing topics",
        "icon": "🔍"
    },
    {
        "id": "first_completion",
        "name": "Achiever",
        "description": "Completed your first investing topic",
        "icon": "🏆"
    },
    {
        "id": "five_completions",
        "name": "Master",
        "description": "Completed 5 different investing topics",
        "icon": "🎓"
    },
    {
        "id": "all_basics",
        "name": "Foundation Builder",
        "description": "Completed all basic investing topics",
        "icon": "🧱"
    },
    {
        "id": "all_advanced",
        "name": "Investment Guru",
        "description": "Completed all advanced investing topics",
        "icon": "🧠"
    }
]

# Badge categories
BADGE_CATEGORIES = [
    {
        "id": "progress",
        "name": "Learning Progress",
        "description": "Badges earned by progressing through investing topics"
    },
    {
        "id": "achievement",
        "name": "Achievements",
        "description": "Badges earned by completing specific achievements"
    }
]

# Map badges to categories
BADGE_CATEGORY_MAP = {
    "first_topic": "progress",
    "five_topics": "progress",
    "first_completion": "achievement",
    "five_completions": "achievement",
    "all_basics": "achievement",
    "all_advanced": "achievement"
}


def get_badge_by_id(badge_id):
    """Get badge details by ID."""
    for badge in BADGES:
        if badge["id"] == badge_id:
            return badge
    return None


def get_badges_by_category(category_id):
    """Get all badges in a category."""
    return [badge for badge in BADGES if BADGE_CATEGORY_MAP.get(badge["id"]) == category_id]


def get_all_badges():
    """Get all available badges."""
    return BADGES
