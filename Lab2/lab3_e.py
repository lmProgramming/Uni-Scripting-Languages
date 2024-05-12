from helper_functions import only_x_answer_logs

if __name__ == '__main__':
    for log in only_x_answer_logs(200):
        print(log.rstrip())