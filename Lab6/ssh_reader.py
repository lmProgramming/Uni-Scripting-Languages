from dataclasses import dataclass
import datetime
from ssh_log import *
from ssh_log_journal import SSHLogJournal
from ssh_user import SSHUser
from random import shuffle

def main():
    journal: SSHLogJournal = SSHLogJournal()
    
    with open("6/OpenSSH_2k.log", "r") as f:
        for line in f:
            journal.append(line)
            
    users: List[SSHUser] = []
    
    users.append(SSHUser("webmaster", datetime.datetime(2024, 12, 10, 9, 16, 24)))
    users.append(SSHUser("test9", datetime.datetime(2024, 12, 10, 10, 17, 25)))
            
    #for log in journal[2:7:2]:
    #    print(log)
        
    #print(journal[IPV4("187.141.143.180")])
    logs = journal[datetime.datetime(2024, 12, 10, 9, 16, 24)]
    
    logs_and_users = users + logs
    shuffle(logs_and_users)
    
    for duck in logs_and_users:
        print(duck)
        print(duck.validate())                    
            
if __name__ == "__main__":
    main()