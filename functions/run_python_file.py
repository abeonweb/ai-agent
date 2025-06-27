import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        full_work_dir = os.path.abspath(working_directory)
        if not full_file_path.startswith(full_work_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'
        timeout = 30
        args = [f"python3 {full_file_path}"]
        result = subprocess.run(args, cwd=working_directory, capture_output=True, timeout=timeout, shell=True, text=True)
        output = ""
        if result.stderr:
            output += f"STDERR: {result.stderr}"
        if result.returncode > 0:
            output += f" Process exited with code {result.returncode}"
        if result.stdout:
            output += f"STDOUT: {result.stdout}"
        if result.stdout =="":
            output = "No output produced."
        return output
    except Exception as e:
        f"Error: executing Python file: {e}"