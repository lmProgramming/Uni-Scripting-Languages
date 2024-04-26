from datetime import datetime
import re

'''
a. Utwórz klasę SSHUser reprezentującą użytkownika. Niech klasa pozwala na
przechowywanie informacji o nazwie użytkownika i dacie ostatniego logowania.
Zdefiniuj w niej metodę validate() , która będzie walidować poprawność nazwy4
użytkownika.
b. Następnie pobierz kilka instancji SSHLogEntry z SSHLogJournal. Utwórz kilka
instancji klasy SSHUser. Przechowaj wszystkie instancje na wspólnej liście.
c. Zademonstruj działanie kaczego typowania poprzez iterację po tej liście i
wywoływanie metody validate() na obiektach różnego typu.
4 np.przypomocywyrażeniaregularnegor'^[a-z_][a-z0-9_-]{0,31}$'
3
'''

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