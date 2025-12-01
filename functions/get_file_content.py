import os
from config import FILE_CHAR_LIMIT


def get_file_content(working_directory, file_path):
    # Construct the absolute path to the file
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    # Check if the file is within the working directory
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the file exists and is a file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Try to read the file content
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read()
        # If the file exceeds the configured character limit, truncate and append a message
        if len(content) > FILE_CHAR_LIMIT:
            content = content[:FILE_CHAR_LIMIT] + f'[...File "{file_path}" truncated at {FILE_CHAR_LIMIT} characters]'
        return content
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_file_content = {
    "name": "get_file_content",
    "description": "Get the content of a file within the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "working_directory": {
                "type": "string",
                "description": "The base working directory from which to read the file.",
            },
            "file_path": {
                "type": "string",
                "description": "The relative path to the file within the working directory.",
            },
        },
        "required": ["file_path"],
    },
}   