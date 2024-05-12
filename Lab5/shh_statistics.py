import random
import statistics
from shh_reader import print_logs
from shh_details_reader import read_details, get_user_from_log, Message, ShhLog
from typing import List, Dict, Tuple

def get_n_random_logs(user_logs, n):
    return random.sample(user_logs, min(n, len(user_logs)))

def logs_to_user_dict(logs):
    log_dict = {}
    for log in logs:
        user = get_user_from_log(log.unparsed_log)
        if user is not None:
            log_dict.setdefault(user, []).append(log)
    return log_dict

def get_n_random_logs_from_random_user(logs_by_users, n: int) -> List[ShhLog]:   
    user_logs = random.choice(list(logs_by_users.values()))
    return get_n_random_logs(user_logs, n)

def calculate_ssh_statistics(logs: List[ShhLog], logs_by_user) -> Dict[str, Dict[str, float]]:
    all_durations = [(log.date, log) for log in logs if log.message == Message.Success or log.message == Message.Disconnected]

    for user, user_logs in logs_by_user.items():
        durations = [(log, user_logs[i+1].date - log.date) for i, log in enumerate(user_logs) 
                    if i+1 < len(user_logs) and (user_logs[i+1].message in [Message.Disconnected, Message.Success, Message.WrongPassword, Message.WrongUsername])]
        if durations:
            mean_duration = statistics.mean(d[1].total_seconds() for d in durations)
            
            print()
            print(f"Statistics for user {user}:")
            print(f"Mean duration: {mean_duration}")
            if len(durations) > 1:                
                std_dev_duration = statistics.stdev(d[1].total_seconds() for d in durations)
                print(f"Standard deviation: {std_dev_duration}")

    durations = [(all_durations[i][0], all_durations[i+1][0] - all_durations[i][0]) 
                for i in range(len(all_durations)-1) 
                if all_durations[i+1][1].message == Message.Disconnected]
    
    if durations:
        mean_duration = statistics.mean(d[1].total_seconds() for d in durations)
        std_dev_duration = statistics.stdev(d[1].total_seconds() for d in durations)
        
        print()        
        print("Overall statistics:")
        print(f"Mean duration: {mean_duration}")
        print(f"Standard deviation: {std_dev_duration}")

def find_least_and_most_frequent_users(logs_by_user) -> Tuple[str, str]:
    least_frequent_user = min(logs_by_user, key=lambda k: len(logs_by_user[k]))
    most_frequent_user = max(logs_by_user, key=lambda k: len(logs_by_user[k]))
    
    return least_frequent_user, most_frequent_user

if __name__ == "__main__":
    logs = read_details("OpenSSH_2k.log")
    
    logs_by_user = logs_to_user_dict(logs)
    
    n = int(input("Input n (integer): "))
    
    print_logs(get_n_random_logs_from_random_user(logs_by_user, n))
    
    calculate_ssh_statistics(logs, logs_by_user)
    
    least_frequent_user, most_frequent_user = find_least_and_most_frequent_users(logs_by_user)
    
    print(f"Least frequent user: {least_frequent_user}")
    print(f"Most frequent user: {most_frequent_user}")
    