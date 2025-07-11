import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info,  get_files_info
from functions.run_python import schema_run_python_file, run_python_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    args = function_call_part.args
    function_name = function_call_part.name

    args["working_directory"] = "./calculator"
    function_result = ""
    match function_name:
        case "get_files_info":
            function_result = get_files_info(**args)
        case "write_file":
            function_result = write_file(**args)
        case "get_file_content":
            function_result = get_file_content(**args)
        case "run_python_file":
            function_result = run_python_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def main():
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = genai.Client(api_key=api_key)

	if len(sys.argv) < 2:
		print("Usage: python3 main.py <content>")
		sys.exit(1)

	user_prompt = sys.argv[1]
	system_prompt = """
	You are a helpful AI coding agent.

	When a user asks a question or makes a request, you must immediately make a function call plan. You can perform the following operations, use the available functions provided as tools:

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

			function_call_found = False

			for candidate in response.candidates:
				messages.append(candidate.content)

				for part in candidate.content.parts:
					if hasattr(part, "function_call") and part.function_call:
						function_call_found = True
						function_call_result = call_function(part.function_call, verbose)
						if  not function_call_result.parts[0].function_response.response:
							raise Exception(f"no result calling {part.function_call.name}({part.function_call.args})")
						if verbose:
							print(f"-> {function_call_result.parts[0].function_response.response}")
						messages.append(function_call_result)
						break
						
				if function_call_found:
					break


			if not function_call_found:
				# No more tool calls - model is finished
				print('\nFinal response:')
				if response.text:
					print(response.text)
				break

		except Exception as e:
			print(f"error: {e}")


if __name__ == "__main__":
	main()
