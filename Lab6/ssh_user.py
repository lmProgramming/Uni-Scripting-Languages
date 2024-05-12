from datetime import datetime
import re

class SSHUser:
    username: str
    last_login: datetime

    def __init__(self, username: str, last_login: datetime):
        self.username = username
        self.last_login = last_login

    def validate(self):
        if self.username in ["root", "admin", "user"]:
            return False
        pattern = r'^[a-z_][a-z0-9_-]{0,31}$'
        return re.match(pattern, self.username) is not None
    
    def __str__(self) -> str:
        return f"I'm a user! My name is: {self.username}, my last login: {self.last_login}"
        
    def __repr__(self) -> str:
        return str(self)