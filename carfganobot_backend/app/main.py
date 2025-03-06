from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from app.routers import chat, users, progress
from app.db.database import engine, Base
from app.db.models import User, UserProgress, UserBadge
from app.auth.security import get_current_active_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CarfganoBot API",
    description="API for the CarfganoBot investing-learning chatbot",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(chat.router)
app.include_router(users.router)
app.include_router(progress.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to the CarfganoBot API",
        "description": "API for the CarfganoBot investing-learning chatbot by Carfgano Enterprises",
        "endpoints": {
            "topics": "/api/chat/topics",
            "topic": "/api/chat/topic",
            "message": "/api/chat/message",
            "users": "/api/users",
            "progress": "/api/progress"
        }
    }

@app.get("/authenticated")
async def authenticated_route(current_user: User = Depends(get_current_active_user)):
    """Test endpoint to verify authentication."""
    return {"message": f"Hello, {current_user.name or current_user.email}!"}
