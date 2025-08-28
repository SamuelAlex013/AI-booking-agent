"""
Optimized FastAPI Backend for AI Calendar Booking Agent
Handles chat requests and provides health monitoring
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import logging
from fastapi.responses import RedirectResponse
from fastapi import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import pathlib
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path for agent import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

logger.info(f"Current directory: {current_dir}")
logger.info(f"Parent directory: {parent_dir}")
logger.info(f"Python path: {sys.path}")

# Check for credentials file
credentials_path = os.path.join(parent_dir, "credentials", "credentials.json")
logger.info(f"Looking for credentials at: {credentials_path}")
logger.info(f"Credentials file exists: {os.path.exists(credentials_path)}")

# Check environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")
logger.info(f"GOOGLE_API_KEY set: {'Yes' if google_api_key else 'No'}")

chat_with_agent = None
clear_conversation_history = None
try:
    from agent import chat_with_agent, clear_conversation_history
    AGENT_AVAILABLE = True
    logger.info("✅ Agent imported successfully")
except ImportError as e:
    AGENT_AVAILABLE = False
    logger.error(f"⚠️ Agent not available: {e}")
    logger.error(f"Available files in parent dir: {os.listdir(parent_dir) if os.path.exists(parent_dir) else 'Directory not found'}")
except Exception as e:
    AGENT_AVAILABLE = False
    logger.error(f"⚠️ Unexpected error importing agent: {e}")

# In-memory user token store (for demo; use DB in production)
user_tokens = {}

# Google OAuth2 client config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://ai-booking-agent.vercel.app/auth/callback")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

# Health check endpoint - must be robust
@app.get("/health")
async def health_check():
    """System health and status check with debugging info"""
    try:
        health_info = {
            "status": "healthy",
            "service": "AI Calendar Booking Agent",
            "version": "2.0.0",
            "agent_available": AGENT_AVAILABLE,
            "endpoints": ["/health", "/chat", "/reset"],
            "environment": "production" if os.getenv("RAILWAY_ENVIRONMENT") else "development"
        }
        
        # Add debugging information if agent is not available
        if not AGENT_AVAILABLE:
            health_info["debug"] = {
                "credentials_exists": os.path.exists(credentials_path),
                "google_api_key_set": bool(google_api_key),
                "current_dir": current_dir,
                "parent_dir": parent_dir,
                "parent_dir_exists": os.path.exists(parent_dir),
                "available_files": os.listdir(parent_dir) if os.path.exists(parent_dir) else "Directory not accessible"
            }
        
        return health_info
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "AI Calendar Booking Agent"
        }

# Main chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Process chat messages through the AI agent"""
    try:
        if not AGENT_AVAILABLE:
            logger.error("AI agent is not available - check credentials and environment")
            raise HTTPException(
                status_code=503, 
                detail={
                    "error": "AI agent is not available",
                    "debug": {
                        "credentials_exists": os.path.exists(credentials_path),
                        "google_api_key_set": bool(google_api_key),
                        "agent_available": AGENT_AVAILABLE
                    }
                }
            )
        
        if not callable(chat_with_agent):
            logger.error("chat_with_agent is not callable")
            raise HTTPException(
                status_code=503,
                detail="AI agent function is not available"
            )
        response = chat_with_agent(request.message)
        return {"response": response}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        return {"response": response, "status": "success"}

# Reset conversation endpoint
@app.post("/reset")
async def reset_conversation():
    """Reset conversation history"""
    if not AGENT_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI agent is not available")
    
    try:
        if 'clear_conversation_history' in globals() and callable(globals().get('clear_conversation_history')):
            globals()['clear_conversation_history']()
            return {"status": "success", "message": "Conversation history cleared"}
        else:
            raise HTTPException(status_code=503, detail="clear_conversation_history function is not available")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset error: {str(e)}")

# Simple status endpoint that always works
@app.get("/")
async def root():
    """Simple root endpoint for basic connectivity test"""
    return {
        "message": "AI Calendar Booking Agent API",
        "version": "2.0.0",
        "status": "running",
        "health_endpoint": "/health"
    }

@app.get("/auth/login")
def login(request: Request):
    """Initiate Google OAuth2 login flow"""
    flow = Flow.from_client_secrets_file(
        str(pathlib.Path(parent_dir) / "credentials" / "client.json"),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    # Store state in session/cookie for CSRF protection (skipped for demo)
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def auth_callback(request: Request, code: Optional[str] = None, state: Optional[str] = None):
    """Handle Google OAuth2 callback and store user tokens"""
    flow = Flow.from_client_secrets_file(
        str(pathlib.Path(parent_dir) / "credentials" / "client.json"),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # For demo: use email as user_id (in production, use proper user management)
    from googleapiclient.discovery import build
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    user_id = user_info.get('email')
    user_tokens[user_id] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return {"message": "Login successful", "user": user_id}

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
