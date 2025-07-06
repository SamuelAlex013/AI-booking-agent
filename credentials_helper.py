"""
Alternative credentials handler for Railway deployment
Uses environment variable if file upload fails
"""
import os
import json
import tempfile

def get_credentials_path():
    """Get credentials file path, creating from env var if needed"""
    # First try the normal file path
    normal_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "credentials.json")
    
    if os.path.exists(normal_path):
        return normal_path
    
    # If normal path doesn't exist, try to create from environment variable
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if credentials_json:
        # Create a temporary file with the credentials
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "credentials.json")
        
        with open(temp_path, 'w') as f:
            if credentials_json.startswith('{'):
                # Already JSON string
                f.write(credentials_json)
            else:
                # Assume it's base64 encoded
                import base64
                decoded = base64.b64decode(credentials_json).decode('utf-8')
                f.write(decoded)
        
        return temp_path
    
    raise FileNotFoundError("No credentials file found and GOOGLE_CREDENTIALS_JSON not set")

# For backwards compatibility
CREDENTIALS_PATH = get_credentials_path()
