import os
from google.genai import types

def get_file_content(working_directory, file_path):

    try:
       # join and resolve the full path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # security check to prevent access outside working_directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # check if path is a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # read and return content
        MAX_CHARS = 10000
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read(MAX_CHARS)
                if len(content) >= MAX_CHARS:
                    return f'{content} [...File "{file_path}" truncated at 10000 characters]'
                return content
            
        except UnicodeDecodeError:
            return f'Error: Could not decode file "{file_path}" with UTF-8'
        
    except Exception as e:
        return f"Error: {str(e)}"
    
# schema for Gemini tooling 
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file as text, contrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get content from, relative the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
