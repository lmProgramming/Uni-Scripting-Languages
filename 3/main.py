from log_parser import read_line
from log_filterer import *
from log_dictionary import *
from log_sorter import *

def read_log(filename):
    logs = []
    with open(filename, "r", encoding="latin") as f:
        for line in f:
            logs.append(read_line(line.rstrip()))
    return logs
            

if __name__ == '__main__':
    test_case = 0
    
    logs = read_log("3/NASA")    
    
    if test_case == 0:    
        logs = get_entries_by_extension(logs, ".html")
        logs = get_entries_by_addr(logs, 'firewall.dfw.ibm.com')
        logs = sort_logs(logs, 6, True)
        print_entries(logs, 10)
    elif test_case == 1:    
        logs = get_entries_by_addr(logs, "burger.letters.com")
        
        log_dict = log_to_dict(logs)
        print_dict_entry_dates(log_dict)
    