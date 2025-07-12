import os
from google.genai import types

def write_file(working_directory, file_path, content):

    try:
        # join and resolve the full path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # security check to prevent access outside working directory
        if full_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # create a directory if doesn't exists
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # writes the updated content
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
        except UnicodeDecodeError:
            return f'Error: Could not encode content for "{file_path}" with UTF-8'
        
    except Exception as e:
        return f"Error: {str(e)}"
    
# schema for Gemini tooling 
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description="Writes content to a specified file, create one if deos not exists, constrianed to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)
