from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# map Gemini function names to actual python functions
available_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call_part: types.FunctionCall, verbose=False):
    """ 
    handles a Gemini function_call_part object.

    args:
        function_call_part (types.FunctionCall): includes .name and .args (dict)
        verbose (bool): if True, prints full arguments list
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # copy args and set working directory to "calculator"
    args = function_call_part.args
    args["working_directory"] = "./calculator"

    # check if function name is invalid return an error
    if not function_call_part.name in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    try:
        # loop up and call the function
        func = available_functions[function_call_part.name]
        function_result = func(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result}
                )
            ]
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": str(e)}
                )
            ]
        )
