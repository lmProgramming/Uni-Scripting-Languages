from enum import Enum, auto

class Message(Enum):
    Success = auto()
    FailedPassword = auto()
    Error = auto()
    Other = auto()