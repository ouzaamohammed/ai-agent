import os
import subprocess

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
            capture_output=True
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
