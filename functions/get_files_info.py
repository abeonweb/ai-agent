import os

def get_files_info(working_directory, directory=None):
    full_work_dir = os.path.abspath(working_directory)
    full_path = ""
    if directory:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
    else:
        full_path = full_work_dir
    if not full_path.startswith(full_work_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path) :
        return f'Error: "{directory}" is not a directory'
    
    wd_list = os.listdir(full_path)
    dir_contents = []
    try:
        for item in wd_list:
            final_full_path = os.path.abspath(os.path.join(full_path, item))
            dir_contents.append(f"- {item}: file_size={os.path.getsize(final_full_path)} bytes, is_dir={os.path.isdir(final_full_path)}")
        
        return "\n".join(dir_contents)
    except FileNotFoundError:
        return f"Error: {directory} file not found"
    except PermissionError:
        return f"Error: You do not have permissions for this file: {directory}"
    except Exception:
            return "Error: An unexpected error occurred"