import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # If the absolutel path to the directory is outside the working directory, return a string error message:
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    #if the directory is not a directory, return a string error message:
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    # Build and return a string representing the conternts of the directory. Format should be "- Filename: file_size, is_dir=False"
    # If any errors are raised by the standard library functions, catch them and instead return a string describing the error. Always prefix error strings with "Error:".
    try:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    except Exception as e:
        return f"Error: {str(e)}"   
    files_info = []
    for filename in os.listdir(abs_directory):
        file_path = os.path.join(abs_directory, filename)
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        files_info.append(f"- {filename}: {file_size} bytes, is_dir={is_dir}")
    return "\n".join(files_info)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)