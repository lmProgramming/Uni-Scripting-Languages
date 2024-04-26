from datetime import datetime
from dataclasses import dataclass

'''
● adres/nazwę hosta, który wykonywał żądanie, 
● znacznik czasu w formacie "DAY/MON/YYY DD HH:MM:SS [TZ]", 
● metodę protokołu HTTP wraz z ścieżką do żądanego zasobu, 
● kod odpowiedzi HTTP (200 – w przypadku dostępności zasobu, 302 – zasób przeniesiony 
tymczasowo, 404 – gdy nie znaleziono), 
● liczbę bajtów w odpowiedzi.
'''

@dataclass
class HTTPCommand:
    command_type: str
    command_path: str
    http_method: str
    
@dataclass
class HTTPAnswer:
    answer_code: str
    answer_length: int | None

def get_host(log: str) -> str:
    return log.split(" ")[0]

def get_time(log: str) -> datetime:
    date_time_unparsed = log.split("[")[1].split("]")[0]
    
    return datetime.strptime(date_time_unparsed, "%d/%b/%Y:%H:%M:%S %z")

def get_http_command(log: str) -> HTTPCommand:
    command_arguments = log.split("\"")[1].split(" ")
    
    try:
        command = command_arguments[0]
        command_path = command_arguments[1]
    
        http_method = ""
        if len(command_arguments) > 2:
            http_method = command_arguments[2]
            
        return HTTPCommand(command, command_path, http_method)
    except IndexError:
        return HTTPCommand("", "", "")    
    
def get_answer(log: str) -> HTTPAnswer:
    line_split = log.split(" ")
    
    answer_code = int(line_split[-2])
    
    try:
        answer_length = int(line_split[-1])    
    except ValueError: 
        answer_length = None
    
    return HTTPAnswer(answer_code, answer_length)
    
def read_line(log: str):
    host = get_host(log)

    date_time = get_time(log)
    
    http_command = get_http_command(log)
    
    http_answer = get_answer(log)
    
    return (host, 
            date_time, 
            http_command.command_type, 
            http_command.command_path, 
            http_command.http_method, 
            http_answer.answer_code, 
            http_answer.answer_length)
    