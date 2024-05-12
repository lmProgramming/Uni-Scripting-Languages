import sys
import log_parser

def only_night_logs():
    for log in sys.stdin:
        date_and_time = log_parser.get_time(log)
        
        hour = date_and_time.time().hour
        if hour > 22 or hour < 6:
            print(log.rstrip())

if __name__ == '__main__':
    only_night_logs()