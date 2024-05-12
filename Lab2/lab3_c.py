import sys
from log_parser import get_answer, get_http_command

def calculate_biggest_log():      
    biggest_log = max(sys.stdin, key=lambda log: get_answer(log).answer_length, default=None)
    
    if biggest_log is not None:
        http_command = get_http_command(biggest_log)
        if http_command is not None:
                print("biggest log\npath:", http_command.command_path, "\nsize:", get_answer(biggest_log).answer_length)
        
if __name__ == "__main__":
    calculate_biggest_log()