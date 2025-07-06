# AI Calendar Assistant

A conversational AI agent for managing Google Calendar through natural language intera## Troubleshootingtions. This appl## Technical Architecture

- **Frontend**: Streamlit web application for user interface
- **Backend**: FastAPI server providing RESTful endpoints
- **AI Engine**: LangChain framework with Google Gemini integration
- **Calendar API**: Google Calendar API v3 for calendar operations
- **Authentication**: Google service account authentication

## Requirements

Key dependencies include:
- `langchain`: AI framework for conversational agents
- `google-generativeai`: Google Gemini AI integration
- `google-api-python-client`: Google Calendar API client
- `fastapi`: Modern web framework for API development
- `streamlit`: Web application framework
- `uvicorn`: ASGI server implementationlows users to schedule, modify, and query calendar events using simple text commands instead of traditional calendar interfaces.

## Features

- **Natural Language Processing**: Uses Google's Gemini AI to understand and respond to calendar requests in plain English
- **Google Calendar Integration**: Direct integration with Google Calendar API for real-time calendar management
- **Conversational Memory**: Maintains context throughout conversations for follow-up commands
- **Web Interface**: Browser-based chat interface built with Streamlit
- **RESTful API**: FastAPI backend for scalable deployment
- **Conflict Detection**: Automatically identifies scheduling conflicts and suggests alternatives

## Project Structure

```
AI-booking-agent/
├── agent.py              # Core AI agent implementation
├── backend/main.py       # FastAPI server
├── frontend/app.py       # Streamlit web interface
├── credentials/          # Google service account credentials
├── requirements.txt      # Python dependencies
├── test_optimized.py     # Test suite
├── start_backend.bat     # Windows backend launcher
└── start_frontend.bat    # Windows frontend launcher
```

## Setup Instructions

### 1. Google AI API Configuration

1. Navigate to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Generate a new API key
3. Save the API key for environment configuration

### 2. Google Calendar API Setup

1. Access [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create a service account with Calendar access permissions
5. Download the service account JSON credentials
6. Place the credentials file in `credentials/credentials.json`
7. Share your Google Calendar with the service account email address

### 3. Installation

```bash
git clone <repository-url>
cd AI-booking-agent
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Running the Application

**Windows:**
```cmd
start_backend.bat
start_frontend.bat
```

**Linux/macOS:**
```bash
# Terminal 1
uvicorn backend.main:app --reload

# Terminal 2
streamlit run frontend/app.py
```

Access the application at `http://localhost:8501`

## Deployment

### Railway

1. Fork the repository on GitHub
2. Create an account at [railway.app](https://railway.app)
3. Connect your GitHub repository
4. Configure environment variables:
   - `GOOGLE_API_KEY`: Your Google AI API key
5. Upload `credentials.json` to the credentials directory

### Alternative Platforms

- **Render**: Suitable for applications requiring persistent storage
- **Fly.io**: Recommended for global deployment with edge computing

## Usage Examples

The application supports natural language queries for calendar management:

- "What meetings do I have today?"
- "Schedule a team standup for tomorrow at 9 AM"
- "Am I available Friday afternoon?"
- "Cancel my 3 PM meeting"
- "Find a free hour next week for a client call"

The conversational agent maintains context, allowing for follow-up commands without repeating information.

