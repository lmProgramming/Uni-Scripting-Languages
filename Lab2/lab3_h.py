import sys
import log_parser

def only_polish_logs():
    for log in sys.stdin:
        host = log_parser.get_host(log)
        
        if host.endswith(".pl"):
            print(log.rstrip())

if __name__ == '__main__':
    only_polish_logs()