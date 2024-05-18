from typing import Iterator, List
from ssh_log import SSHLogEntryError, SSHLogEntryOther, SSHLogEntryPasswordAccepted, SSHLogEntryPasswordRejected
from ssh_log import SSHLogEntry, IPv4Address
from datetime import datetime
from typing import Callable

class SSHLogJournal:
    logs: List[SSHLogEntry]

    def __init__(self) -> None:
        self.logs = []

    def __len__(self) -> int:
        return len(self.logs)

    def __iter__(self) -> Iterator[SSHLogEntry]:
        return iter(self.logs)

    def __contains__(self, item: SSHLogEntry) -> bool:
        return item in self.logs

    def append(self, log: str) -> None:
        entry: SSHLogEntryPasswordRejected | SSHLogEntryError | SSHLogEntryPasswordAccepted | SSHLogEntryOther = SSHLogEntry.create_specific_log(log)
        if entry.validate():
            self.logs.append(entry)
        else:
            raise ValueError("Invalid log entry: {log}")

    def get_logs_by_criteria(self, criteria: Callable[[SSHLogEntry], bool]) -> List[SSHLogEntry]:
        return [log for log in self.logs if criteria(log)]

    def get_logs_by_octet(self, ip: IPv4Address, octet_index: int) -> List[SSHLogEntry]:
        return self.get_logs_by_criteria(lambda log: log.ip is not None and log.ip.get_octet(octet_index) == ip)
    
    def __getitem__(self, key: slice | int | IPv4Address | datetime) -> List[SSHLogEntry]:
        if isinstance(key, slice):
            return self.logs[key]
        elif isinstance(key, int):
            return [self.logs[key]]
        elif isinstance(key, IPv4Address):
            return [log for log in self.logs if log.ipv4 == key]
        elif isinstance(key, datetime):
            return [log for log in self.logs if log.timestamp == key]            
        else:
            raise TypeError("Invalid key type. Expected slice or tuple or IPV4 or datetime.")