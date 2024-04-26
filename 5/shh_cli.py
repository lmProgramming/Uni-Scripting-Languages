import argparse
from shh_reader import print_logs
from shh_details_reader import read_details, get_ipv4s_from_log
from shh_statistics import *
import logging_ssh

def main():
    parser = argparse.ArgumentParser(description="SSH Log Analysis Tool")
    parser.add_argument("log_file", help="Path to the SSH log file")
    parser.add_argument("--min_log_level", help="Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL), default=DEBUG", 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default="DEBUG")

    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="additional help")

    random_parser = subparsers.add_parser("random", help="Select random entries for random/specified user")
    random_parser.add_argument("n", type=int, help="Number of random entries to select")
    random_parser.add_argument("user", type=str, help="Specify user", nargs="?")
    random_parser.set_defaults(which="random")
    
    ipv4_parser = subparsers.add_parser("ipv4", help="Get ipv4s from logs")
    ipv4_parser.set_defaults(which="ipv4")    

    stats_parser = subparsers.add_parser("stats", help="Calculate SSH statistics")
    stats_parser.set_defaults(which="stats")

    frequency_parser = subparsers.add_parser("frequency", help="Find least and most frequent users")
    frequency_parser.set_defaults(which="frequency")    

    args = parser.parse_args()

    logs = read_details(args.log_file)
        
    logs_by_user = logs_to_user_dict(logs)
    
    if not hasattr(args, "which"):
        logging_ssh.setup_logging(args.min_log_level)
        logging_ssh.log_information(logs)
        
        return   
    
    subparser_chosen = args.which
        
    if subparser_chosen == "random":
        n = args.n
        
        if args.user:
            print_logs(get_n_random_logs(logs_to_user_dict[args.user], n))
        else:
            print_logs(get_n_random_logs_from_random_user(logs_by_user, n))
    elif subparser_chosen == "stats":
        calculate_ssh_statistics(logs, logs_by_user)
    elif subparser_chosen == "frequency":
        least_frequent_user, most_frequent_user = find_least_and_most_frequent_users(logs_by_user)
    
        print(f"Least frequent user: {least_frequent_user}")
        print(f"Most frequent user: {most_frequent_user}")
    elif subparser_chosen == "ivp4":
        print(set([get_ipv4s_from_log(log) for log in logs]))        
        
if __name__ == "__main__":
    main()