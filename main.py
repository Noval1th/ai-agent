import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key loaded: {api_key is not None}")

# Initialize the GenAI client
client = genai.Client(api_key=api_key)

# Parse command-line arguments (positional prompt + optional --verbose flag)
parser = argparse.ArgumentParser(description="ai-agent: generate content from a prompt")
parser.add_argument("prompt", help="The prompt to send to the model")
parser.add_argument("--verbose", "-v", action="store_true", help="Show prompt and token counts")
args = parser.parse_args()

contents = args.prompt
verbose = args.verbose

messages = [
    types.Content(role="user", parts=[types.Part(text=contents)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,schema_write_file,schema_run_python_file
    ]
)

def main():
    print("Hello from ai-agent!")
    system_prompt = """
                    You are a helpful AI coding agent.

                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files

                    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
                    """
    output = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt))
    
    # Check for function calls
    if output.function_calls:
        for function_call_part in output.function_calls:
            # Inject working_directory into the function call
            result = call_function(function_call_part, working_directory="./calculator")
            print(f"Result: {result}")
    else:
        print(output.text)
    
    if verbose:
        # Show the user prompt and token usage only when verbose is enabled
        print("--- Verbose Info ---")
        print(f"User prompt: {contents}")
        try:
            prompt_tokens = output.usage_metadata.prompt_token_count
        except Exception:
            prompt_tokens = getattr(output.usage_metadata, 'prompt_token_count', None)
        try:
            response_tokens = output.usage_metadata.candidates_token_count
        except Exception:
            response_tokens = getattr(output.usage_metadata, 'candidates_token_count', None)
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
