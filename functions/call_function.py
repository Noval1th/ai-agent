from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False, working_directory=None):

    function_name = function_call_part.name
    args = dict(function_call_part.args or {})
    # Inject working_directory if provided
    if working_directory:
        args["working_directory"] = working_directory
    
    if verbose:
        print(f"Calling function: {function_name}({args})")
        print(f"Function result: {result}")  
    else:
        print(f" - Calling function: {function_name}")
    
    # Dispatch to the appropriate function
    if function_name == "get_files_info":
        working_dir = args.get("working_directory", ".")
        path = args.get("path", ".")
        result = get_files_info(working_dir, path)
    elif function_name == "get_file_content":
        working_dir = args.get("working_directory", ".")
        file_path = args.get("file_path")
        if not file_path:
            return "Error: 'file_path' argument is required."
        result = get_file_content(working_dir, file_path)
    elif function_name == "write_file":
        working_dir = args.get("working_directory", ".")
        file_path = args.get("file_path")
        content = args.get("content", "")
        if not file_path:
            return "Error: 'file_path' argument is required."
        result = write_file(working_dir, file_path, content)
    elif function_name == "run_python_file":
        working_dir = args.get("working_directory", ".")
        file_path = args.get("file_path")
        arguments = args.get("arguments", [])
        if not file_path:
            return "Error: 'file_path' argument is required."
        result = run_python_file(working_dir, file_path, arguments)
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
    


    return result