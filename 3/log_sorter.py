def sort_logs(logs, index_to_sort_by, ascending=False):
    try:
        return sorted(logs, key=lambda x: x[index_to_sort_by], reverse=ascending)
    except IndexError:
        print("Index out of range. Please provide a valid index.")
        return logs