from typing import List
from ssh_log import SSHLogEntry, IPv4Address
from datetime import datetime

class SSHLogJournal:
    logs: List[SSHLogEntry]

    def __init__(self):
        self.logs = []

    def __len__(self):
        return len(self.logs)

    def __iter__(self):
        return iter(self.logs)

    def __contains__(self, item):
        return item in self.logs

    def append(self, log: str):
        entry = SSHLogEntry.create_specific_log(log)
        if entry.validate():
            self.logs.append(entry)
        else:
            raise ValueError("Invalid log entry: {log}")

    def get_logs_by_criteria(self, criteria):
        return [log for log in self.logs if criteria(log)]
    
    def __repr__(self) -> str:
        return f"Contains {len(self.logs)} logs"
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.logs[key]
        elif isinstance(key, int):
            return self.logs[key]
        elif isinstance(key, IPv4Address):
            return [log for log in self.logs if log.ipv4 == key]
        elif isinstance(key, datetime):
            return [log for log in self.logs if log.timestamp == key]            
        else:
            raise TypeError("Invalid key type. Expected slice or tuple or IPV4 or datetime.")