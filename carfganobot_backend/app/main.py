from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from app.routers import chat

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
            "message": "/api/chat/message"
        }
    }
