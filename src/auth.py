"""
User authentication (register, login, created)

This module provides functionalities for user authentication including
registration, login, and account creation.

Functions:
    register_user(username: str, password: str) -> bool:
        Registers a new user with the provided username and password.
        
    login_user(username: str, password: str) -> bool:
        Authenticates a user with the provided username and password.
        
    create_account(username: str, password: str) -> bool:
        Creates a new account for the user with the provided username and password.
"""

import os
from utils import hash_password
import string
import random
import json
from datetime import datetime, timedelta

AUTH_FILE = "auth_data.json"

def _load_user_data():
    """Load user data from JSON file

    Returns:
        dict: A dictionary containing user data.
    """
    try:
        with open(AUTH_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}} # Ensure users key exists
    
def _save_user_data(data: dict):
    """Save user data to JSON file

    Args:
        data (dict): user data

    Returns:
        dict: contains all user data such as username, password, session token etc.
    """
    with open(AUTH_FILE, 'w') as file:
        return json.dump(data, file, indent=4)

def create_account(username: str, password: str, role='user'):
    """Create new user with a hashed password

    Args:
        username (str): username
        password (str): password
        role (str, optional): user role. Defaults to 'user'.

    Returns:
        bool: True if user doesn't exist, False if user already exist.
    """
    data = _load_user_data()
    
    if username in data["users"]:
        print(f"User {username} already exists.\nProvide a new username.")
        return False
    
    data["users"][username] = {
        "password": hash_password(password),
        "role": role,
        "session_token": None, # Session token assigned only after login
        "expires_at": None
    }
    
    _save_user_data(data)
    print(f"User '{username}' created successfully.")
    return True

def verify_user(username: str, password: str):
    """Verify user credentials during login

    Args:
        username (str): user name
        password (str): password

    Returns:
        bool: True if the credentials are valid, False otherwise
    """
    user_data = _load_user_data(AUTH_FILE)
    hashed_password = hash_password(password)
    return user_data.get(username, {}).get('password') == hashed_password

def generate_session_token():
    """Generate a random session token

    Returns:
        str: A randomly generated session token.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))