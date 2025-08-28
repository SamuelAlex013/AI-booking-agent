"""
Vercel serverless function entry point for FastAPI
"""
from api.main import app

# For Vercel deployment
handler = app
application = app
