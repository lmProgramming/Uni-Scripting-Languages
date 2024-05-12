from dataclasses import dataclass
import datetime
import re
from enum import Enum, auto
from typing import Optional

class Message(Enum):
    Success = auto()
    UnableToLogIn = auto()
    Disconnected = auto()
    WrongPassword = auto()
    WrongUsername = auto()
    BreakInAttempt = auto()
    Other = auto()

@dataclass
class ShhLog:
    unparsed_log: str
    date: datetime.datetime
    server_name: str
    event: int
    details: str
    message: Optional[Message] = None
    user: Optional[str] = None

'''
Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!
Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186
Dec 10 06:55:46 LabSZ sshd[24200]: input_userauth_request: invalid user webmaster [preauth]
Dec 10 06:55:46 LabSZ sshd[24200]: pam_unix(sshd:auth): check pass; user unknown
Dec 10 06:55:46 LabSZ sshd[24200]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=173.234.31.186 
Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2
'''
def parse_log(log_unparsed: str) -> ShhLog:
    pattern = r'(?P<datetime>\S{3}\s+\d{1,2}\s+\d\d:\d\d:\d\d)\s+(?P<servername>\S{5})\s+sshd\[(?P<event>\d+)\]:\s+(?P<details>.*)'

    matches = re.fullmatch(pattern, log_unparsed.strip())
    
    date = datetime.datetime.strptime(matches["datetime"], "%b %d %H:%M:%S")
    server_name = matches["servername"]
    event = matches["event"]
    details = matches["details"]
    
    log = ShhLog(log_unparsed.strip(), date, server_name, event, details)
    
    return log    
    
    
def read_logs(logs_path: str):
    logs = []
    
    with open(logs_path, "r") as logs_unparsed:
        for log_unparsed in logs_unparsed:
            log = parse_log(log_unparsed)
            logs.append(log)
            
    return logs

def print_logs(logs):
    for log in logs:
        print(log.unparsed_log)

if __name__ == "__main__":
    read_logs("OpenSSH_2k.log")