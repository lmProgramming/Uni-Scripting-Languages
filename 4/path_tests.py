import os
import sys

def get_path_directories():
    directories = os.getenv("PATH").split(os.pathsep)
    
    return directories
        
def print_path_directories():
    path_directories = get_path_directories()
    for directory in path_directories:
        print(directory)

def print_executables_in_path():    
    directories = get_path_directories()
    for directory in directories:
        print(directory + ":")
        try:
            files = os.listdir(directory)
            executables = [file for file in files if os.access(os.path.join(directory, file), os.X_OK)]
            for exe in executables:
                print(f"\t {exe}")
        except FileNotFoundError:
            print("Directory not found.")
        except PermissionError:
            print("Permission denied.")

if __name__ == "__main__":
    show_executables = sys.argv[1] if len(sys.argv) > 1 else False
        
    if show_executables:
        print_executables_in_path()
    else:
        print_path_directories()