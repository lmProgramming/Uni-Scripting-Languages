import typer
from shh_reader import print_logs
from shh_details_reader import read_details, get_ipv4s_from_log
from shh_statistics import *
import logging_ssh

app = typer.Typer()

@app.command()
def random(n: int, user: str = None, log_file: str = typer.Argument(...)):
    logs = read_details(log_file)
    logs_by_user = logs_to_user_dict(logs)

    if user:
        print_logs(get_n_random_logs(logs_to_user_dict[user], n))
    else:
        print_logs(get_n_random_logs_from_random_user(logs_by_user, n))

@app.command()
def stats(log_file: str = typer.Argument(...)):
    logs = read_details(log_file)
    logs_by_user = logs_to_user_dict(logs)

    calculate_ssh_statistics(logs, logs_by_user)

@app.command()
def frequency(log_file: str = typer.Argument(...)):
    logs = read_details(log_file)
    logs_by_user = logs_to_user_dict(logs)

    least_frequent_user, most_frequent_user = find_least_and_most_frequent_users(logs_by_user)

    typer.echo(f"Least frequent user: {least_frequent_user}")
    typer.echo(f"Most frequent user: {most_frequent_user}")

@app.command()
def ipv4(log_file: str = typer.Argument(...)):
    logs = read_details(log_file)

    ipv4s = set(get_ipv4s_from_log(log.unparsed_log) for log in logs)
    typer.echo(ipv4s)
    
@app.command()
def log(log_file: str = typer.Argument(...), min_log_level: str = "DEBUG"):
    logs = read_details(log_file)
    
    logging_ssh.setup_logging(min_log_level)
    logging_ssh.log_information(logs)

if __name__ == "__main__":
    app()
