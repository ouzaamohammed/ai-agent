import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    target_directory = working_directory
    if directory:
        target_directory = os.path.join(working_directory, directory)

    if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    
    file_info = []
    try:
        for filename in os.listdir(target_directory):
            file_size = os.path.getsize(os.path.join(target_directory, filename))
            is_dir = os.path.isdir(os.path.join(target_directory, filename))
            file_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
    except Exception as e:
        return f"Error: {e}"
        
    return "\n".join(file_info)

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
