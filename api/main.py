"""
Lightweight FastAPI Backend for Vercel Deployment
Optimized version with minimal dependencies
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Configure Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI(
    title="AI Calendar Booking Agent",
    description="Conversational AI for Google Calendar management",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Simplified calendar service
def get_calendar_service():
    """Get Google Calendar service"""
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not credentials_json:
        raise Exception("No credentials found")
    
    credentials_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict, 
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    return build('calendar', 'v3', credentials=credentials)

# Simple AI chat function
def simple_chat(message: str) -> str:
    """Simple AI chat using Google Gemini"""
    try:
        if not GOOGLE_API_KEY:
            return "AI service is not configured. Please check your API key."
        
        model = GenerativeModel('gemini-2.0-flash-exp')
        
        # Simple calendar context
        prompt = f"""You are an AI calendar assistant. The user said: "{message}"
        
        Respond helpfully about calendar management. If they want to:
        - Check calendar: Say "I can help you check your calendar events"
        - Book appointment: Say "I can help you schedule that appointment"
        - General chat: Respond naturally about calendar management
        
        Keep responses brief and helpful."""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"I'm having trouble processing your request. Error: {str(e)}"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Calendar Booking Agent (Vercel)",
        "version": "2.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Calendar Booking Agent API (Vercel)",
        "version": "2.0.0",
        "status": "running"
    }

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Simple chat endpoint"""
    try:
        response = simple_chat(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vercel handler
handler = app
