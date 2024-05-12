import re
from typing import List
from shh_reader import ShhLog, read_logs, Message

def get_ipv4s_from_log(log: str):
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    matched = re.search(pattern, log)
    if matched:
        return matched[0]

def get_user_from_log(log: str):
    pattern = r'\s+user(?:\s*=\s*| )([^ ]+)'
    matched = re.search(pattern, log)
    if matched:        
        user = matched.group(1)
        if user == 'unknown':
            return None
        return user

def get_message_type(log: ShhLog):
    message_types = {
        'Accepted password': Message.Success,
        'authentication failure': Message.UnableToLogIn,
        'Received disconnect': Message.Disconnected,
        'Connection closed': Message.Disconnected,
        'Failed password': Message.WrongPassword,
        'Invalid user': Message.WrongUsername,
        'user unknown': Message.WrongUsername,
        'POSSIBLE BREAK-IN ATTEMPT!': Message.BreakInAttempt,
        'other': Message.Other
    }
    
    for pattern in message_types.keys():
        matched = re.search(pattern, log.details)
        if matched is not None:
            return message_types[pattern]
    return message_types['other']

def read_details(logs_path: str):
    logs: List[ShhLog] = read_logs(logs_path)
        
    for log in logs:
        log.message = get_message_type(log)
        log.user = get_user_from_log(log.unparsed_log)
        
    return logs

if __name__ == "__main__":
    read_details("OpenSSH_2k.log")