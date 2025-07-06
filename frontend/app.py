import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="AI Calendar Booking Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app styling - Full screen */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        min-height: 100vh;
        padding: 0;
        margin: 0;
    }
    
    /* Main container */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    }
    
    /* Enhanced chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: slideIn 0.4s ease-out;
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 80%;
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateY(20px) scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white !important;
        border: none;
        margin-left: auto;
        margin-right: 1rem;
        position: relative;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
    }
    
    .user-message::after {
        content: '';
        position: absolute;
        top: 20px;
        right: -15px;
        width: 0;
        height: 0;
        border-top: 15px solid transparent;
        border-bottom: 15px solid transparent;
        border-left: 15px solid #00f2fe;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #1a202c !important;
        border: none;
        margin-right: auto;
        margin-left: 1rem;
        position: relative;
        box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);
    }
    
    .bot-message::after {
        content: '';
        position: absolute;
        top: 20px;
        left: -15px;
        width: 0;
        height: 0;
        border-top: 15px solid transparent;
        border-bottom: 15px solid transparent;
        border-right: 15px solid #43e97b;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        border-radius: 25px;
        margin-bottom: 3rem;
        color: white;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Feature box styling */
    .feature-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: white !important;
        backdrop-filter: blur(15px);
    }
    
    /* Status indicator styling */
    .status-indicator {
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 600;
        display: inline-block;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
    }
    
    .status-online {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1a202c !important;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .status-offline {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #8b4513 !important;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Chat input fixes - Enhanced for perfect visibility */
    .stChatInput {
        background: transparent !important;
        border-radius: 30px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3) !important;
        margin: 2rem 0 !important;
        border: none !important;
    }
    
    .stChatInput > div {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 30px !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2) !important;
    }
    
    .stChatInput > div > div {
        background: transparent !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stChatInput input,
    .stChatInput > div > div > input,
    .stChatInput textarea,
    .stChatInput > div > div > textarea {
        color: #2c3e50 !important;
        background-color: transparent !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 18px 30px !important;
        caret-color: #667eea !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .stChatInput input:focus,
    .stChatInput > div > div > input:focus,
    .stChatInput textarea:focus,
    .stChatInput > div > div > textarea:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background-color: transparent !important;
    }
    
    .stChatInput input::placeholder,
    .stChatInput > div > div > input::placeholder,
    .stChatInput textarea::placeholder,
    .stChatInput > div > div > textarea::placeholder {
        color: #4a5568 !important;
        font-style: italic !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Fix for any remaining white artifacts */
    .stChatInput * {
        background: transparent !important;
        border: none !important;
    }
    
    .stChatInput > div:first-child {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 30px !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
    }
    
    /* General text styling for full screen */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: white !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: white !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* Spinner styling */
    .stSpinner {
        color: white !important;
    }
    
    .stSpinner > div {
        border-color: white transparent white transparent !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        color: white;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(15px);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.2) 100%);
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Remove default Streamlit padding */
    .css-18e3th9 {
        padding-top: 0 !important;
    }
    
    .css-1d391kg {
        padding-top: 0 !important;
    }
    
    /* Hide Streamlit menu and footer for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "http://127.0.0.1:8000"  # Change this for deployment

def check_backend_status():
    """Check if the backend is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_message_to_agent(message):
    """Send message to the booking agent"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"response": f"Error: Server returned status {response.status_code}", "status": "error"}
    except requests.exceptions.ConnectionError:
        return {"response": "❌ Cannot connect to the backend server. Please make sure it's running on http://127.0.0.1:8000", "status": "error"}
    except requests.exceptions.Timeout:
        return {"response": "⏱️ Request timed out. The agent might be processing a complex request.", "status": "error"}
    except Exception as e:
        return {"response": f"❌ Unexpected error: {str(e)}", "status": "error"}

def reset_conversation():
    """Reset the conversation history"""
    try:
        response = requests.post(f"{API_URL}/reset", timeout=10)
        return response.status_code == 200
    except:
        return False

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# Header
st.markdown("""
<div class="header-container">
    <h1>📅 AI Calendar Booking Assistant</h1>
    <p>Your intelligent assistant for managing calendar appointments</p>
</div>
""", unsafe_allow_html=True)

# Backend status check
backend_online = check_backend_status()
status_class = "status-online" if backend_online else "status-offline"
status_text = "🟢 Backend Online" if backend_online else "🔴 Backend Offline"

col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    st.markdown(f'<div class="status-indicator {status_class}">{status_text}</div>', unsafe_allow_html=True)

if not backend_online:
    st.error("⚠️ The backend server is not running. Please start it with: `uvicorn backend.main:app --reload`")
    st.stop()

# Features overview
with st.expander("✨ What I can help you with", expanded=not st.session_state.conversation_started):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>📋 Check Availability</h4>
            <p>Ask me about your calendar availability for any date</p>
            <small><em>"Am I free tomorrow?"</em></small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>⏰ Suggest Times</h4>
            <p>Get smart suggestions for available meeting slots</p>
            <small><em>"Suggest times for Monday"</em></small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h4>📝 Book Appointments</h4>
            <p>Schedule meetings and appointments effortlessly</p>
            <small><em>"Book a team meeting"</em></small>
        </div>
        """, unsafe_allow_html=True)

# Chat interface
st.markdown("""
<div class="chat-container">
    <h3 style="color: #2c3e50; text-align: center; margin-bottom: 1rem;">💬 Chat with your AI Assistant</h3>
</div>
""", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    message_class = "user-message" if message["role"] == "user" else "bot-message"
    icon = "👤" if message["role"] == "user" else "🤖"
    
    # Convert \n to <br> for proper line breaks
    formatted_content = message["content"].replace("\\n", "<br>").replace("\n", "<br>")
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <strong style="color: inherit;">{icon} {"You" if message["role"] == "user" else "AI Assistant"}:</strong><br>
        <span style="color: inherit;">{formatted_content}</span>
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("✨ Ask me anything about your calendar... (e.g., 'Am I free tomorrow?' or 'Book a meeting with John at 3pm')")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversation_started = True
    
    # Display user message immediately
    user_formatted = user_input.replace("\\n", "<br>").replace("\n", "<br>")
    st.markdown(f"""
    <div class="chat-message user-message">
        <strong style="color: inherit;">👤 You:</strong><br>
        <span style="color: inherit;">{user_formatted}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Show thinking indicator
    with st.spinner("🤔 AI Assistant is thinking..."):
        # Send message to agent
        response = send_message_to_agent(user_input)
    
    # Add assistant response to chat history
    assistant_response = response.get("response", "Sorry, I couldn't process your request.")
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Display assistant response
    response_formatted = assistant_response.replace("\\n", "<br>").replace("\n", "<br>")
    st.markdown(f"""
    <div class="chat-message bot-message">
        <strong style="color: inherit;">🤖 AI Assistant:</strong><br>
        <span style="color: inherit;">{response_formatted}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Rerun to update the chat
    st.rerun()

# Sidebar with additional options
with st.sidebar:
    st.markdown("### 🛠️ Options")
    
    if st.button("🔄 Reset Conversation"):
        if reset_conversation():
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.success("Conversation reset!")
            st.rerun()
        else:
            st.error("Failed to reset conversation")
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Quick Examples
    Try asking:
    - "Hello, I need help booking a meeting"
    - "Am I available on July 8th?"
    - "Suggest some times for next Monday"
    - "Book a doctor's appointment for tomorrow at 2 PM"
    - "What meetings do I have this week?"
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### ℹ️ About
    This AI assistant helps you manage your Google Calendar through natural conversation.
    
    **Features:**
    - Natural language understanding
    - Real-time calendar integration
    - Smart time slot suggestions
    - Seamless appointment booking
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>AI Calendar Booking Assistant | Powered by LangChain & Google Calendar API</small>
</div>
""", unsafe_allow_html=True)

# Auto-scroll to bottom when new messages are added
if st.session_state.messages:
    st.markdown("""
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    """, unsafe_allow_html=True)
