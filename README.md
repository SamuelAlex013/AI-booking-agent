# AI Calendar Assistant

A conversational AI agent for managing Google Calendar through natural language interactions. This application allows users to schedule, modify, and query calendar events using simple text commands instead of traditional calendar interfaces.

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

### Railway (Recommended)

This project is pre-configured for Railway deployment:

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the configuration

3. **Environment Variables**
   In Railway dashboard, add:
   - `GOOGLE_API_KEY`: Your Google AI API key
   - `PYTHONPATH`: `/app`

4. **Upload Credentials**
   - In Railway dashboard, go to Files
   - Create `credentials` folder
   - Upload your `credentials.json` file

5. **Custom Domain (Optional)**
   - In Railway dashboard, go to Settings
   - Add custom domain or use the generated Railway domain

### Alternative Platforms

- **Render**: Add a `render.yaml` configuration file
- **Fly.io**: Use `fly launch` to generate configuration
- **Heroku**: Use existing Procfile configuration

## Live Demo

Once deployed, your application will be available at your Railway domain. The API endpoints include:

- `GET /health` - Health check endpoint
- `POST /chat` - Main chat interface
- `POST /clear` - Clear conversation history

## Usage Examples

The application supports natural language queries for calendar management:

- "What meetings do I have today?"
- "Schedule a team standup for tomorrow at 9 AM"
- "Am I available Friday afternoon?"
- "Cancel my 3 PM meeting"
- "Find a free hour next week for a client call"

The conversational agent maintains context, allowing for follow-up commands without repeating information.

## Troubleshooting

### Deployment Issues

**Railway deployment fails:**
- Verify all environment variables are set
- Check that `credentials.json` is uploaded correctly
- Review build logs in Railway dashboard

**Service fails to start:**
- Verify Python 3.8+ in railway.toml
- Confirm Google AI API key is valid
- Check Railway service logs

### API Issues

**AI not responding:**
- Check API rate limits and quota usage
- Verify environment variables in Railway
- Review application logs

### Testing

Run the test suite locally before deployment:
```bash
python test_optimized.py
```

## Technical Architecture

- **Frontend**: Streamlit web application (local development)
- **Backend**: FastAPI server providing RESTful endpoints
- **AI Engine**: LangChain framework with Google Gemini integration
- **Calendar API**: Google Calendar API v3 for calendar operations
- **Authentication**: Google service account authentication
- **Deployment**: Railway with automatic builds and deployments

## Requirements

Key dependencies include:
- `langchain`: AI framework for conversational agents
- `google-generativeai`: Google Gemini AI integration
- `google-api-python-client`: Google Calendar API client
- `fastapi`: Modern web framework for API development
- `streamlit`: Web application framework
- `uvicorn`: ASGI server implementation

## Contributing

This project welcomes contributions. Please follow standard Git workflow:

1. Fork the repository
2. Create a feature branch
3. Implement changes with appropriate tests
4. Submit a pull request with detailed description

## License

This project is licensed under the MIT License.

