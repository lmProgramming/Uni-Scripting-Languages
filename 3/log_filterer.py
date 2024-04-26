'''199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245'''

def filter_logs(logs: list, index_to_check: int, filter_function):
    return [log for log in logs if filter_function(log[index_to_check])]    

def get_entries_by_addr(logs: list, address: str) -> list:
    return filter_logs(logs, 0, lambda x: x == address)

def get_entries_by_code(logs: list, code: str) -> list:
    return filter_logs(logs, 5, lambda x: x == code)

def get_failed_reads(logs: list, merge: bool = True):
    error_4xx = filter_logs(logs, 5, lambda x: 400 <= x < 500)
    error_5xx = filter_logs(logs, 5, lambda x: 500 <= x < 600)
    
    if merge:
        return error_4xx + error_5xx
    else:
        return error_4xx, error_5xx

def get_entries_by_extension(logs: list, extension: str) -> list:
    return filter_logs(logs, 3, lambda x: x.endswith(extension))

def print_entries(logs: list, count=None):
    for log in logs:
        if count is not None:
            count -= 1
            if count == 0:
                break
        print(log)