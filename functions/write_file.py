import os

def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        full_work_dir = os.path.abspath(working_directory)
        if not full_file_path.startswith(full_work_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        dir_name = os.path.dirname(full_file_path)
        print(f"dir_name: {dir_name}")
        full_dir_path = os.path.abspath(os.path.join(working_directory, dir_name))
        os.makedirs(full_dir_path, exist_ok=True)
        with open(full_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except FileNotFoundError:
            return f"Error: {file_path} file not found"
    except PermissionError:
        return f"Error: You do not have permissions for this file: {file_path}"
    except IOError:
        return "Error: An I/O error occurred"
    except OSError:
        return "Error: An OS error occurred"
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    