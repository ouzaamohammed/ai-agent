import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", file_path],
            cwd=working_directory,
            capture_output=True,
            timeout=30
        )
        outputs = []
        if result.stdout:
            outputs.append(f"STDOUT:\n {result.stdout}") 
        if result.stderr:
            outputs.append(f"STDERR:\n {result.stderr}")
        if result.returncode != 0:
            outputs.append(f"Process exited with code {result.returncode}")
        return "\n".join(outputs) if outputs else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within a specified working directory, enforcing safety checks and a 30-second timeout, and returns the captured output or errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute, within the working directory.",
            ),
        },
    ),
)