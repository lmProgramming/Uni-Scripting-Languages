import datetime
import re
from message import Message
from typing import List, Literal
from enum import Enum, auto
from abc import ABC, abstractmethod
from ipaddress import IPv4Address

class SSHLogEntry(ABC):
    timestamp: datetime.datetime
    server_name: str
    event: int
    details: str
    user: str | None = None
    ipv4: IPv4Address | None = None
    _unparsed_log: str
    
    @abstractmethod
    def validate(self) -> bool:
        pass
    
    def __init__(self, unparsed_log: str) -> None:
        self._unparsed_log = unparsed_log
        
        self.base_parse_log()
        
        self.ipv4 = SSHLogEntry.get_ipv4s_from_log(self.details)
        self.user = SSHLogEntry.get_user_from_log(self.details)
        self.message: Message = SSHLogEntry.get_message(self.details)
        
    @property
    def has_ip(self) -> bool:
        return self.ipv4 is not None
    
    def base_parse_log(self) -> None:
        pattern = r'(?P<datetime>\S{3}\s+\d{1,2}\s+\d\d:\d\d:\d\d)\s+(?P<servername>\S+)\s+sshd\[(?P<event>\d+)\]:\s+(?P<details>.*)'

        matches: re.Match[str] | None = re.fullmatch(pattern, self._unparsed_log.strip())
        
        if matches is None:
            raise ValueError("Invalid log entry")
        self.timestamp = datetime.datetime.strptime(matches["datetime"], "%b %d %H:%M:%S").replace(year=2024)
        self.server_name = matches["servername"]
        self.event = int(matches["event"])
        self.details = matches["details"]

    @staticmethod
    def get_ipv4s_from_log(details: str) -> IPv4Address | None:
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        matched: re.Match[str] | None = re.search(pattern, details)
        if matched:
            return IPv4Address(matched[0])
        return None

    @staticmethod
    def get_user_from_log(details: str) -> None | str:
        pattern = r'\s+user(?:\s*=\s*| )([^ ]+)'
        matched: re.Match[str] | None = re.search(pattern, details)
        if matched:        
            user: str = matched.group(1)
            if user == 'unknown' or user == 'authentication':
                return None
            return user
        return None
    
    @staticmethod
    def create_specific_log(unparsed_log: str):
        message: Message = SSHLogEntry.get_message(unparsed_log)
        
        if message == Message.FailedPassword:
            return SSHLogEntryPasswordRejected(unparsed_log)
        elif message == Message.Error:
            return SSHLogEntryError(unparsed_log)
        elif message == Message.Success:
            return SSHLogEntryPasswordAccepted(unparsed_log)
        else:
            return SSHLogEntryOther(unparsed_log)
        
    @staticmethod
    def get_message(details: str) -> Message:
        message_types: dict[str, Message] = {
            'POSSIBLE BREAK-IN ATTEMPT!': Message.Other,            
            'accepted password': Message.Success,
            'authentication failure': Message.Error,
            'error': Message.Error,
            'Received disconnect': Message.Error,
            'Connection closed': Message.Error,
            'Failed password': Message.FailedPassword,
            'Invalid user': Message.Error,
            'user unknown': Message.Error,
        }
        
        for pattern in message_types.keys():
            matched: re.Match[str] | None = re.search(pattern, details, re.IGNORECASE)
            if matched is not None:
                return message_types[pattern]
        return Message.Other
    
    def __str__(self) -> str:
        return f'{self.timestamp} {self.server_name} {self.event} {self.user} {self.ipv4} {self.message}'
    
    def __repr__(self) -> str:
        return f'{__class__.__name__}({self._unparsed_log})'

    def __eq__(self, other) -> bool:
        if isinstance(other, SSHLogEntry):
            return self._unparsed_log == other._unparsed_log
        return False

    def __lt__(self, other) -> bool:
        if isinstance(other, SSHLogEntry):
            return self.timestamp < other.timestamp
        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, SSHLogEntry):
            return self.timestamp > other.timestamp
        return NotImplemented
    
class SSHLogEntryPasswordRejected(SSHLogEntry):
    port: int
    ssh_type: str
    
    def __init__(self, unparsed_log: str) -> None:
        super().__init__(unparsed_log)
        self.port, self.ssh_type = SSHLogEntryPasswordAccepted.get_specific_details(self.details)    
        
    @staticmethod
    def get_specific_details(details) -> tuple[int, str]:
        pattern = r'port\s+(?P<port>\d+) (?P<ssh_type>\S+)'
        matches: re.Match[str] | None = re.search(pattern, details)
        
        if matches:            
            port: int = int(matches['port'])
            ssh_type: str = matches['ssh_type']   
            
            return port, ssh_type
        raise ValueError("Didn't provide a log that accepts/rejects a password")
        
    def validate(self) -> bool:
        try:
            other_port, other_ssh_type = SSHLogEntryPasswordAccepted.get_specific_details(self._unparsed_log)    
        
            return self.port == other_port and self.ssh_type == other_ssh_type
        except ValueError:
            return False
    
    def __str__(self) -> str:
        return "PasswordRejected! " + super().__str__() + f'\nPort: {self.port} ssh_type: {self.ssh_type}'

class SSHLogEntryPasswordAccepted(SSHLogEntry):    
    port: int
    ssh_type: str
    
    def __init__(self, unparsed_log: str) -> None:
        super().__init__(unparsed_log)   
        self.port, self.ssh_type = SSHLogEntryPasswordAccepted.get_specific_details(self.details)    
    
    @staticmethod
    def get_specific_details(details) -> tuple[int, str]:
        pattern = r'port\s+(?P<port>\d+) (?P<ssh_type>\S+)'
        matches: re.Match[str] | None = re.search(pattern, details)
        
        if matches:            
            port: int = int(matches['port'])
            ssh_type: str = matches['ssh_type']   
            
            return port, ssh_type
        raise ValueError("Didn't provide a log that accepts/rejects a password")
        
    def validate(self) -> bool:
        try:
            other_port, other_ssh_type = SSHLogEntryPasswordAccepted.get_specific_details(self._unparsed_log)    
        
            return self.port == other_port and self.ssh_type == other_ssh_type
        except ValueError:
            return False
        
    def __str__(self) -> str:
        return "PasswordAccepted! " + super().__str__()
 
class Error(Enum):
    Authentication = auto()
    Disconnected = auto()
    InvalidUser = auto()
    Other = auto()

class SSHLogEntryError(SSHLogEntry):         
    error: Error
         
    def __init__(self, unparsed_log: str) -> None:
        super().__init__(unparsed_log)
        self.error = SSHLogEntryError.get_error_type(self.details)
        
    def validate(self) -> bool:        
        other_error: Error = SSHLogEntryError.get_error_type(self._unparsed_log)    
    
        return self.error == other_error
    
    def __str__(self) -> str:
        return "Error! " + super().__str__()
    
    @staticmethod
    def get_error_type(details: str) -> Error:
        message_types: dict[str, Error] = {
            'authentication failure': Error.Authentication,
            'Received disconnect': Error.Disconnected,
            'Connection closed': Error.Disconnected,
            'Invalid user': Error.InvalidUser,
            'user unknown': Error.InvalidUser,
        }
                
        for pattern in message_types.keys():
            matched: re.Match[str] | None = re.search(pattern, details)
            if matched is not None:
                return message_types[pattern]
        return Error.Other

class SSHLogEntryOther(SSHLogEntry):
    def __init__(self, unparsed_log: str) -> None:
        super().__init__(unparsed_log)    
    
    def __str__(self) -> str:
        return "Other! " + super().__str__()
    
    def validate(self) -> Literal[True]:
        return True