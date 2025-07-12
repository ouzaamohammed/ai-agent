import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    try:
        # join and resolve the full path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)


        # security check to prevent access outside working directory
        if full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # check if file exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        # check if file is a python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # excute the file using uv
        result = subprocess.run(
            ["uv", "run", full_path],
            cwd=working_directory,
            capture_output=True,
            timeout=30,
            text=True
        )

        output_lines = []

        if result.stdout.strip():
            output_lines.append(f"STDOUT:\n {result.stdout.strip()}") 

        if result.stderr.strip():
            output_lines.append(f"STDERR:\n {result.stderr.strip()}")

        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        return "\n\n".join(output_lines) if output_lines else "No output produced."
    
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"

# schema for Gemini tooling
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file, constrianed to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative the working directory.",
            ),
        },
        required=["file_path"]
    ),
)