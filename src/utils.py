"""
Helper utilities (hashing, JSON I/O, JSON schema validation.)

Functions:
    hash_string(input_string: str) -> str:
        Generates a SHA-256 hash for the given input string.

    read_json_file(file_path: str) -> dict:
        Reads a JSON file from the specified file path and returns its contents as a dictionary.

    load_json_schema(schema_file: dict) -> bool:
        Loads the JSON schema file that we define for our use case
        
    write_json_file(data: dict, file_path: str) -> None:
        Writes the given dictionary to a JSON file at the specified file path.
        
    validate_json_schema(data: dict, schema: dict) -> bool:
        Validates the given dictionary against the provided JSON schema.
"""
import json
import jsonschema
from jsonschema import validate
import jsonschema.exceptions
import hashlib

def read_json_file(file_path: str):
    """Load user data from JSON file

    Args:
        file_path (str): file path to the JSON file
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def write_json_file(file_path: str, data: dict):
    """Save user data to JSON file

    Args:
        file_path (str): file path to store the JSON file 
        data (dict): user data
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
def load_json_schema(schema_file: dict):
    """Load JSON schema from a file

    Args:
        schema_file (dict): schema for the JSON user data file

    Returns:
        _type_: parsed JSON schema
    """
    with open(schema_file, 'r') as file:
        return json.load(file)
 
def hash_string(password: str):
    """Hash password for secure storage

    Args:
        password (str): user password

    Returns:
        _type_: hexadecimal string
    """
    return hashlib.sha256(password.encode()).hexdigest()

def validate_json_schema(data: dict, schema_file = 'schema.json'):
    """Validate JSON data against the defined schema

    Args:
        data (dict): actual userdata in the form of JSON
        schema_file (str, optional): schema defined for the user data JSON file. Defaults to 'schema.json'.

    Returns:
        _type_: True if data matches the schema, False if data varies from the schema
    """
    schema = load_json_schema(schema_file)
    try:
        validate(instance=data, schema=schema)
        return True, 'JSON is valid'
    except jsonschema.exceptions.ValidationError as e:
        return False, f'JSON validation error: {e.message}'        