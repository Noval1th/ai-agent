import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

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


def main():
    print("Hello from ai-agent!")
    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
    output = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages,config=types.GenerateContentConfig(system_instruction=system_prompt),)
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
