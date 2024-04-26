from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from shh_reader import ShhLog, Message
from shh_details_reader import read_details, get_ipv4s_from_log

def detect_brute_force_attacks(logs: List[ShhLog], max_interval: timedelta, user_to_detect: str=None) -> Dict[Tuple[datetime, str], int]:
    failed_attempts = defaultdict(list)
    
    for log in logs: 
        if not (user_to_detect is None or log.user == user_to_detect):
            continue
            
        if log.message == Message.WrongPassword:            
            ip_address = get_ipv4s_from_log(log.unparsed_log)
            
            last_attempt_list = failed_attempts[ip_address]
            
            if last_attempt_list == []:
                failed_attempts[ip_address].append([log.date])
                continue           
            
            last_timestamp = failed_attempts[ip_address][-1][-1]
            
            if log.date - last_timestamp <= max_interval:
                failed_attempts[ip_address][-1].append(log.date)
            else:
                failed_attempts[ip_address].append([log.date])
    
    brute_force_attempts = [(ip_address, attempt_dates) for ip_address, list_of_date_attempts in failed_attempts.items() 
                            for attempt_dates in list_of_date_attempts]
    
    return brute_force_attempts

def main():
    logs = read_details("OpenSSH_2k.log")

    max_interval = timedelta(seconds=30)

    brute_force_attempts = detect_brute_force_attacks(logs, max_interval)
    print("Detected brute force attempts:")
    for ip_address, attempt_dates in sorted(brute_force_attempts, key=lambda x: len(x[1])):
        timestamp = attempt_dates[-1]
        print(f"Timestamp: {timestamp}, IP Address: {ip_address}, Attempts: {len(attempt_dates)}")
        
if __name__ == "__main__":
    main()