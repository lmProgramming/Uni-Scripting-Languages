from collections import defaultdict

def entry_to_dict(entry: tuple) -> dict:
    fields = ['host', 'datetime', 'command_type', 'command_path', 'http_method', 'answer_code', 'answer_length']
    return dict(zip(fields, entry))

def log_to_dict(logs: list) -> dict:
    log_dict = defaultdict(list)
    for log in logs:
        host, _, _, _, _, _, _ = log
        log_dict[host].append(entry_to_dict(log))
    return dict(log_dict)

def get_addrs(log_dict: dict) -> list:
    return list(log_dict.keys())

def print_dict_entry_dates(log_dict: dict):
    for addr, entries in log_dict.items():
        total_requests = len(entries)
        
        first_request_date = min(entry['datetime'] for entry in entries)
        last_request_date = max(entry['datetime'] for entry in entries)
        
        success_requests = sum(1 for entry in entries if entry['answer_code'] == 200)
        success_rate = success_requests / total_requests if total_requests > 0 else 0
        
        print(f"Address: {addr}")
        print(f"Total requests: {total_requests}")
        print(f"First request date: {first_request_date}")
        print(f"Last request date: {last_request_date}")
        print(f"Success rate: {success_rate:.2%}")
        print()