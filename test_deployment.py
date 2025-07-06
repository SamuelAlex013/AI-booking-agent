#!/usr/bin/env python3
"""
Railway Deployment Test Script
Tests if all components are ready for deployment
"""
import os
import sys

def test_deployment_readiness():
    """Test if the project is ready for Railway deployment"""
    print("🚀 Testing Railway deployment readiness...")
    
    # Test 1: Check if credentials exist
    credentials_path = os.path.join("credentials", "credentials.json")
    if os.path.exists(credentials_path):
        print("✅ Credentials file found")
    else:
        print("❌ Credentials file missing - you need to upload this to Railway")
    
    # Test 2: Check environment variable
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if google_api_key:
        print("✅ GOOGLE_API_KEY environment variable set")
    else:
        print("❌ GOOGLE_API_KEY environment variable missing")
    
    # Test 3: Check if agent can be imported
    try:
        from agent import chat_with_agent
        print("✅ Agent module can be imported")
    except ImportError as e:
        print(f"❌ Agent import failed: {e}")
    
    # Test 4: Check if backend can start
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from backend.main import app
        print("✅ Backend FastAPI app can be created")
    except Exception as e:
        print(f"❌ Backend startup failed: {e}")
    
    # Test 5: Check required files
    required_files = ["requirements.txt", "Procfile", "railway.toml", "agent.py", "backend/main.py"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
    
    print("\n🎯 Deployment checklist:")
    print("1. Push your code to GitHub")
    print("2. In Railway, set GOOGLE_API_KEY environment variable")
    print("3. Upload credentials.json to Railway's file system")
    print("4. Railway will automatically build and deploy")

if __name__ == "__main__":
    test_deployment_readiness()
