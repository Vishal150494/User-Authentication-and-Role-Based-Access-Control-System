"""
User authentication (register, login, logout)

This module provides functionalities for user authentication including
registration, login, and logout.

Classes:
    AuthManager:
        Manages user authentication and session handling.

Functions:
    create_account(username: str, password: str, role='user') -> bool:
        Creates a new account for the user with the provided username, password, and role.
        
    verify_user(username: str, password: str) -> bool:
        Verifies the user's credentials.
        
    login_user(username: str, password: str) -> bool:
        Authenticates a user and returns success or failure.
        
    logout_user(username: str) -> bool:
        Logs out the user by clearing the session token.
"""
import json
from datetime import datetime, timedelta, timezone
from utils import hash_password

AUTH_FILE = "data/auth_data.json"
class AuthManager:
    SESSION_DURATION = 300 # Session expires in 5 minutes (300 seconds)
    
    def __init__(self):
        self.data = self._load_user_data()
        
    def _load_user_data(self):
        """Load user data from JSON file

        Returns:
            dict: A dictionary containing user data.
        """
        try:
            with open(AUTH_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": {}} # Ensure users key exists
        
    def _save_user_data(self):
        """Save user data to JSON file

        Args:
            data (dict): user data

        Returns:
            dict: contains all user data such as username, password, session token etc.
        """
        with open(AUTH_FILE, 'w') as file:
            return json.dump(self.data, file, indent=4)

    def create_account(self, username: str, password: str, role='user'):
        """Create new user with a hashed password

        Args:
            username (str): username
            password (str): password
            role (str, optional): user role. Defaults to 'user'.

        Returns:
            bool: True if user doesn't exist, False if user already exist.
        """
        
        if username in self.data["users"]:
            print(f"User {username} already exists.\nProvide a new username.")
            return False
        
        self.data["users"][username] = {
            "password": hash_password(password),
            "role": role,
            "session_token": None, # Session token assigned only after login
            "expires_at": None
        }
        
        self._save_user_data()
        print(f"User '{username}' created successfully.")
        return True

    def verify_user(self, username: str, password: str):
        """Verify user credentials during login

        Args:
            username (str): user name
            password (str): password

        Returns:
            bool: True if the credentials are valid, False otherwise
        """
        hashed_password = hash_password(password)
        if username not in self.data['users']:
            return False
        
        return self.data['users'][username]['password'] == hashed_password

    def login_user(self, username: str, password: str):
        """Authenticate user and return success or failure

        Args:
            username (str): username
            password (str): password

        Returns:
            bool: True if login is successful, False otherwise.
        """
        
        if username not in self.data['users']:
            print(f"User '{username}' not found")
            return False
        
        if not self.verify_user(username, password):
            print(f"Invalid password.")
            return False
        
        print(f"Login successful for user '{username}'.")
        return True
        
    def logout_user(self, username: str):
        """Log out the user by clearing session token and resetting session duration.

        Args:
            username (str): username

        Returns:
            bool: True if log out is successful, False otherwise
        """
        
        if username in self.data['users']:
            self.data['users'][username]['session_token'] = None
            self.data['users'][username]['expires_at'] = None
            self._save_user_data()
            print(f"User '{username} logged out successfully.")
            return True
            
        print(f"User '{username}' not found.")
        return False