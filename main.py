import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2:
	print("Usage: python3 main.py <content>")
	sys.exit(1)

user_prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
messages = [
  	types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
		schema_write_file,
		schema_get_file_content,
		schema_run_python_file
    ]
)

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
  	model="gemini-2.0-flash-001", 
  	contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if response.function_calls:
	for function_call_part in response.function_calls:
		print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
	print(response.text)

if sys.argv[-1] == "--verbose":
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)