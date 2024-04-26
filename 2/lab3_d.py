import sys
import log_parser

def calculate_ratio_of_graphics():      
    logs = sys.stdin.readlines()
    
    total_graphic = sum(1 for log in logs if log_parser.get_http_command(log).command_path.endswith(
        ('.gif', '.jpg', '.jpeg', '.xbm')))
    
    ratio = total_graphic / len(logs) * 100
    print("ratio:", str(ratio) + "%")
        
if __name__ == "__main__":
    calculate_ratio_of_graphics()