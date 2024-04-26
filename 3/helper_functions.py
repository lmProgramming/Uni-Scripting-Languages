import sys
import log_parser
from typing import List


def bytes_to_gigabytes(bytes: int) -> int:
    return bytes / 1024 // 1024

def filter_and_print_logs(predicate):
    for log in filter(predicate(log), sys.stdin):
        print(log.rstrip())
        
def only_x_answer_logs(x) -> List[str]:
    return list(filter(lambda log : log_parser.get_answer(log).answer_code == x, sys.stdin))