import functools

def make_generator(f: callable):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator

squares = make_generator(lambda x: x**2)()
print(squares)

@functools.lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n == 1:
        return 0
    if n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci_gen = make_generator(fibonacci)()

'''
Korzystając z modułu functools, utwórz funkcję make_generator_mem, która działa
tak, jak make_generator, ale memoizuje funkcję f. Implementację wykonaj w taki
sposób, aby uniknąć duplikowania kodu. Zastanów się, czy możliwa jest memoizacja
funkcji rekurencyjnych i jak ją zrealizować
'''

def make_generator_mem(f: callable):
    f = functools.lru_cache(maxsize=None)(f)
    return make_generator(f)()

def test_generator(gen):
    for i in gen:
        print(i)
        end_if_not_empty = input()
        if end_if_not_empty != "":
            return
        
test_generator(fibonacci_gen)
test_generator(squares)