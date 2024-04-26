import argparse, sys
import time
import os
    
DEFAULT_LINES: int = 10

def tail(lines, n: int=DEFAULT_LINES):
    for line in lines[-n:]:
        print(line)
    
def follow(file_path: str):
    f = open(file_path, "r", encoding="latin")
    f.seek(0, os.SEEK_END)
    
    while True:
        line = f.readline()
        if not line:            
            time.sleep(0.1)
            continue

        yield line
    
if __name__ == "__main__":    
    parser=argparse.ArgumentParser()
    
    parser.add_argument("path", nargs="?")
    parser.add_argument("--lines", help="Specify count of lines to print", default=DEFAULT_LINES, type=int)
    parser.add_argument("--follow", 
                        help="The program, after writing out the contents of the file, does not terminate its \
                            operation, but waits for other processes to add lines to the file, and then displays them", 
                        action="store_true")

    args=parser.parse_args()  
    
    if args.path:
        with open(args.path, "r", encoding="latin") as f:
            dane = f.readlines()
    else:        
        dane = sys.stdin.readlines()  
    
    tail(dane, args.lines)
    
    if args.path and args.follow:  
        loglines = follow(args.path)
        for line in loglines:
            print(line.strip())  
    