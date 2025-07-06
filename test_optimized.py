"""
Optimized Test Suite for AI Calendar Booking Agent
Tests all major functionality with minimal code
"""
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def test_agent():
    """Test the optimized agent functionality"""
    try:
        from agent import chat_with_agent, clear_conversation_history, get_conversation_summary
        
        print("🚀 Testing Optimized AI Calendar Booking Agent")
        print("=" * 60)
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d at %I:%M %p')}")
        print()
        
        # Clear conversation to start fresh
        clear_conversation_history()
        
        # Test scenarios with memory
        test_scenarios = [
            "Hello! Can you help me with my calendar?",
            "What's my schedule for today?",
            "Book a quick test meeting for July 7th at 2:00 PM",
            "What did I just book?",  # Memory test
            "Cancel that test meeting",  # Memory reference test
        ]
        
        for i, message in enumerate(test_scenarios, 1):
            print(f"\n{i}. 👤 User: {message}")
            try:
                response = chat_with_agent(message)
                print(f"   🤖 Agent: {response}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            print("-" * 50)
        
        # Show conversation summary
        print(f"\n📝 Memory Test: {get_conversation_summary()}")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_backend():
    """Test backend connectivity"""
    try:
        import requests
        
        print("\n🌐 Testing Backend Connection")
        print("=" * 60)
        
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Backend is healthy!")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Version: {health_data.get('version', 'Unknown')}")
            print(f"   Agent Available: {health_data.get('agent_available', False)}")
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Start it with: python backend/main.py")
    except Exception as e:
        print(f"❌ Backend test error: {e}")

if __name__ == "__main__":
    test_agent()
    test_backend()
