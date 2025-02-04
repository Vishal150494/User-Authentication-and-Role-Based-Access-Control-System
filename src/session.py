"""
This module defines the SessionManager class, which is responsible for managing user sessions in an authentication system. It inherits from the AuthManager class and provides methods to create, validate, and potentially terminate user sessions.

CLASSES:
    SessionManager: 
        Manages user sessions, including creation and validation.
METHODS:
    __init__: 
        Initializes the SessionManager by calling the parent AuthManager's initializer.
        
    _generate_session_token: 
        Generates a random session token.
        
    create_session: 
        Creates a session for a logged-in user, storing the session token and expiry time.
        
    validate_session: 
        Validates a session token and checks if it has expired.
"""
import random
import string
from datetime import datetime, timedelta, timezone
from auth import AuthManager

class SessionManager(AuthManager):
    def __init__(self):
        super().__init__() # Initializing AuthManager
    
    def _generate_session_token(self):
        """Generate a random session token

        Returns:
            str: A randomly generated session token.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    def create_session(self, username: str):
        """Create a session for a logged in user.

        Args:
            username (str): username

        Returns:
            str: session token if user exists, None otherwise
        """
        if username not in self.data['users']:
            print(f"User '{username} not found.'")
            return None
        
        session_token = self._generate_session_token()
        expiry_time = (datetime.now(timezone.utc) + timedelta(seconds=self.SESSION_DURATION)).isoformat()
        
        #Update session information
        self.data['users'][username]['session_token'] = session_token
        self.data['users'][username]['expires_at'] = expiry_time
        self._save_user_data()
        
        print(f"Session created for user '{username}'. Session token: {session_token}")
        return session_token
        
    def validate_session(self, username: str, session_token: str):
        """Validate session token and check expiry

        Args:
            username (str): username
            session_token (str): session token

        Returns:
            bool: True if session is valid, False otherwise
        """
        if username not in self.data['users']:
            print(f"User '{username}' not found.\nSession cannot be created.")
            return False
        
        user = self.data['users'][username]
        if user['session_token'] != session_token:
            print(f"Invalid session token.")
            return False
        
        expiry_time = datetime.fromisoformat(user['expires_at'])
        if datetime.now(timezone.utc) > expiry_time:
            print(f"Session Expired.")
            return False
        
        print(f"Session is valid.")
        return True
    
    # For future session termination if database structure is implemented
    """def terminate_session(self, username: str):
        pass"""
