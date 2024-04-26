from shh_details_reader import read_details, Message
from shh_reader import ShhLog
from typing import List
import logging

def log_information(logs):        
    for log in logs:
        byte_count = len(log.unparsed_log)
        
        logging.debug(f'Read {byte_count} bytes.')
        
        match log.message:
            case Message.Success:
                logging.info("Successful login or connection closed.")
            case Message.UnableToLogIn | Message.WrongPassword | Message.WrongUsername:
                logging.warning("Failed login attempt.")
            case Message.Disconnected:
                error_logger.error("Error occurred.")
            case Message.BreakInAttempt:
                error_logger.critical("Intrusion attempt detected.")
            case _:
                logging.debug("No specific action for this log entry.")
        
def setup_logging(log_level):
    global error_logger
    
    level = logging.DEBUG    
    match log_level:
        case "INFO":
            level = logging.INFO
        case "WARNING":
            level = logging.WARNING
        case "ERROR":
            level = logging.ERROR
        case "CRITICAL":
            level = logging.CRITICAL
        case _:
            level = logging.DEBUG
    
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')

    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)
    error_logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    logs: List[ShhLog] = read_details("SSH.log")
    
    setup_logging(log_level="INFO")
    
    log_information(logs)