import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        full_work_dir = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_file_path.startswith(full_work_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        timeout = 30
        inputs = ["python3", full_file_path]
        result = subprocess.run(
            inputs, 
            cwd=full_work_dir, 
            capture_output=True, 
            timeout=timeout, 
            text=True
        )
        output = []
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        if result.returncode > 0:
            output.append(f" Process exited with code {result.returncode}")
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if output:
            return "\n".join(output)
        else: 
            return "No output produced."
    except Exception as e:
        f"Error: executing Python file: {e}"