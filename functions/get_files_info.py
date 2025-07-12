import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    # default to working_directory if directory is None
    if directory is None:
        directory = ""

    try:
        # join and resolve the full path
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory = os.path.abspath(working_directory)

        # security check to prevent access outside working_directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # check if path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        # list and describe  each item
        files = os.listdir(full_path)
        lines = []

        for file_name in sorted(files):
            file_path = os.path.join(full_path, file_name)
            try:
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                lines.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")
            except Exception as e:
                lines.append(f"-{file_name}: error getting details {str(e)}")
        
        return "\n".join(lines) if lines else "empty directory"

    except Exception as e:
        return f"Error: {str(e)}"

# schema for Gemini tooling
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
