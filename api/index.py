"""
Vercel serverless function entry point for FastAPI
"""
from backend.main import app

# For Vercel deployment
handler = app
application = app
