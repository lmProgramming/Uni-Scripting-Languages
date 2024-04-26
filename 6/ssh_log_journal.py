from typing import List
from ssh_log import SSHLogEntry, IPV4
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

    def get_logs_by_octet(self, ip, octet_index):
        return self.get_logs_by_criteria(lambda log: log.ip is not None and log.ip.get_octet(octet_index) == ip)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else len(self.logs)
            step = key.step if key.step is not None else 1
            return self.logs[start:stop:step]
        elif isinstance(key, int):
            return [self.logs[key]]
        elif isinstance(key, IPV4):
            return [log for log in self.logs if log.ipv4 == key]
        elif isinstance(key, datetime):
            return [log for log in self.logs if log.timestamp == key]            
        else:
            raise TypeError("Invalid key type. Expected slice or tuple.")