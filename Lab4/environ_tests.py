import os
import sys

def display_environment_variables_with_filter(filter_parameters=None):
    sorted_env_variables = sorted(os.environ.items())

    for key, value in sorted_env_variables:
        if filter_parameters is None or key in filter_parameters:
            print(f"{key}: {value}")

if __name__ == "__main__":
    filter_parameters = sys.argv[1:] if len(sys.argv) > 1 else None
    
    display_environment_variables_with_filter(filter_parameters)
