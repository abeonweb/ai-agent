import os

def get_files_info(working_directory, directory=None):
    full_work_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    wd_list = os.listdir(os.path.abspath(working_directory))
    if not full_path.startswith(full_work_dir) or len(wd_list) == 0 :
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    def get_str(dir, item):
        full_path = os.path.abspath(os.path.join(dir, item))
        return f"- {item}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
    
    def get_format_str(dir, dir_list):
        str=""
        for i in dir_list:
            if i.startswith("__"):
                continue
            str += get_str(dir, i) + "\n"
        return str
    
    abs_directory=""
    if directory == ".":
        return get_format_str(working_directory, wd_list) 
    else:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    # find the dir in working directory
    for dir in wd_list:
        dir = os.path.abspath(os.path.join(working_directory, dir))
        if dir != abs_directory:
            continue
        try:
            if os.path.isfile(dir):
                return f'Error: "{directory}" is not a directory'
            if os.path.isdir(dir):
                # list contents
                dir_list = os.listdir(dir)
                return get_format_str(abs_directory, dir_list)  
        except FileNotFoundError:
            return f"Error: {directory} file not found"
        except PermissionError:
            return f"Error: You do not have permissions for this file: {directory}"
        except Exception:
            return "Error: An unexpected error occurred"
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'