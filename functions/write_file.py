import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(full_path):
            parent_dir = "/".join(full_path.split("/")[:-1])
            os.makedirs(parent_dir, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description="Writes content to a file within a specified working directory, and creating parent directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write, within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content to write to the file.",
            ),
        },
    ),
)
