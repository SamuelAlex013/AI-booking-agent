"""
Optimized FastAPI Backend for AI Calendar Booking Agent
Handles chat requests and provides health monitoring
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys

# Add parent directory to path for agent import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent import chat_with_agent, clear_conversation_history
    AGENT_AVAILABLE = True
except ImportError as e:
    AGENT_AVAILABLE = False
    print(f"⚠️ Agent not available: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="AI Calendar Booking Agent",
    description="Conversational AI for Google Calendar management",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    message: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health and status check"""
    return {
        "status": "healthy",
        "service": "AI Calendar Booking Agent",
        "version": "2.0.0",
        "agent_available": AGENT_AVAILABLE,
        "endpoints": ["/health", "/chat", "/reset"]
    }

# Main chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Process chat messages through the AI agent"""
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI agent is not available")
    
    try:
        response = chat_with_agent(request.message)
        return {"response": response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

# Reset conversation endpoint
@app.post("/reset")
async def reset_conversation():
    """Reset conversation history"""
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI agent is not available")
    
    try:
        clear_conversation_history()
        return {"status": "success", "message": "Conversation history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset error: {str(e)}")

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
