from ssh_log_journal import SSHLogJournal
            
def gather_logs_from(file_path):    
    journal = SSHLogJournal()
    
    with open(file_path, "r") as f:
        for line in f:
            journal.append(line)
        
    return journal