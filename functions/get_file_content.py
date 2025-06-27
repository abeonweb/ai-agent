import os

def get_file_content(working_directory, file_path):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if full_file_path is None or full_file_path == "" or not full_file_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'    
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            MAX_CHARS = 10000
            with open(full_file_path, "r") as f:
                file_content_string = f.read()
                if len(file_content_string) > MAX_CHARS:
                    return file_content_string[0:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
                return file_content_string
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
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'    