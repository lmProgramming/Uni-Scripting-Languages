'''
Zaproponuj implementacje następujących funkcji wyższego rzędu przyjmujących
predykat pred (unarną funkcję zwracającą wartość logiczną), iterable (obiekt, po
którym można iterować) i potencjalnie n - dodatnią liczbę całkowitą.
a. forall(pred, iterable) - funkcja zwraca True, jeśli każdy element
iterable spełnia predykat pred, w przeciwnym przypadku False,
b. exists(pred, iterable) – funkcja zwraca True, jeśli co najmniej jeden
element iterable spełnia predykat pred, w przeciwnym przypadku False,
c. atleast(n, pred, iterable) – funkcja zwraca True, jeśli co najmniej n
elementów iterable spełnia predykat pred, w przeciwnym przypadku False.
d. atmost(n, pred, iterable) – funkcja zwraca True, jeśli co najwyżej n
elementów iterable spełnia predykat pred, w przeciwnym przypadku False.
'''

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
                return True
    return False

print(forall(lambda x: x > 0, [1, 2, 3, 4, 5]))
print(forall(lambda x: x > 0, [1, 2, 3, -4, 5]))

print(exists(lambda x: x < 0, [1, 2, 3, 4, 5]))
print(exists(lambda x: x < 0, [1, 2, 3, -4, 5]))

print(atleast(5, lambda x: x > 0, [1, 2, 3, 4, 5]))
print(atleast(5, lambda x: x > 0, [1, 2, 3, -4, 5]))