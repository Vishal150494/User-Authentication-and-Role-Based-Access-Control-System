"""
Helper utilities (hashing, JSON I/O, etc.)

Functions:
    hash_string(input_string: str) -> str:
        Generates a SHA-256 hash for the given input string.

    read_json_file(file_path: str) -> dict:
        Reads a JSON file from the specified file path and returns its contents as a dictionary.

    write_json_file(data: dict, file_path: str) -> None:
        Writes the given dictionary to a JSON file at the specified file path.

    validate_json_schema(data: dict, schema: dict) -> bool:
        Validates the given dictionary against the provided JSON schema.
"""