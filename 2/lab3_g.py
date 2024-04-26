import sys
import log_parser

def only_friday_logs():
    for log in sys.stdin:
        date_and_time = log_parser.get_time(log)
        
        if date_and_time.weekday() == 4:
            print(log.rstrip())

if __name__ == '__main__':
    only_friday_logs()