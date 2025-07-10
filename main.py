import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
	print("Usage: python3 main.py <content>")
	sys.exit(1)

user_prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations, use the available functions provided as tools:

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

verbose = sys.argv[-1] == "--verbose"

MAX_ITERATIONS = 20
for _ in range(MAX_ITERATIONS):
	try:
		response = client.models.generate_content(
			model="gemini-2.0-flash-001", 
			contents=messages,
			config=types.GenerateContentConfig(
				tools=[available_functions], system_instruction=system_prompt
			),
		)

		if response.text:
			print("Final response:")
			print(response.text)
			break

		for candidate in response.candidates:
			messages.append(candidate.content)

		if response.function_calls:
			# function_responses = []
			for function_call_part in response.function_calls:
				function_call_result = call_function(function_call_part, verbose)
				if  not function_call_result.parts[0].function_response.response:
					raise Exception(f"no result calling {function_call_part.name}({function_call_part.args})")

				print(f"function responses: {function_call_result.parts[0].function_response}")

				messages.append(function_call_result)
				# function_responses.append(function_call_result.parts[0])

				if verbose:
					print(f"-> {function_call_result.parts[0].function_response.response}")

				# if not function_call_result:
				# 	print("Final response:")
				# 	print(response.text)
				# 	break

			# messages.append(types.Content(
			# 	role="tool",
			# 	parts=function_responses
			# ))
		
	except Exception as e:
		print(f"error: {e}")
