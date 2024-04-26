import sys
import log_parser
import helper_functions

def main():  
    sum_of_answer_bytes = sum(log_parser.get_answer(log).answer_length for log in sys.stdin)    
        
    print(helper_functions.bytes_to_gigabytes(sum_of_answer_bytes), "gigabytes")
        
if __name__ == "__main__":
    main()