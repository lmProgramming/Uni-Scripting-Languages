def forall(pred, iterable):
    for element in iterable:
        if not pred(element):
            return False
    return True

def exists(pred, iterable):
    for element in iterable:
        if pred(element):
            return True
    return False    

def atleast(n, pred, iterable):
    count = 0
    for element in iterable:
        if pred(element):
            count += 1
            if count >= n:
                return False
    return True

def atmost(n, pred, iterable):
    count = 0
    for element in iterable:
        if pred(element):
            count += 1
            if count > n:
                return True
    return False

if __name__ == "__main__":
    print("forall")
    print(forall(lambda x: x > 0, [1, 2, 3, 4, 5]))
    print(forall(lambda x: x > 0, [1, 2, 3, -4, 5]))

    print("exists")
    print(exists(lambda x: x < 0, [1, 2, 3, 4, 5]))
    print(exists(lambda x: x < 0, [1, 2, 3, -4, 5]))

    print("atleast")
    print(atleast(5, lambda x: x > 0, [1, 2, 3, 4, 5]))
    print(atleast(5, lambda x: x > 0, [1, 2, 3, -4, 5]))

    print("atmost")
    print(atmost(4, lambda x: x > 0, [1, 2, 3, 4, 5]))
    print(atmost(4, lambda x: x > 0, [1, 2, 3, -4, 5]))