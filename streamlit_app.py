"""
Main entry point for Streamlit deployment
This allows deploying the frontend from the root directory
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main frontend app
from frontend.app import main

if __name__ == "__main__":
    main()
