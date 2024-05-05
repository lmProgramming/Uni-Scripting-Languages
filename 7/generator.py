import functools
import sys
from typing import Callable

def make_generator(f: Callable):
    n = 1
    while True:
        yield f(n)
        n += 1

def fibonacci(n: int) -> int:
    if n == 1:
        return 0
    if n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def make_generator_mem_naive(f: Callable):
    @functools.cache
    def f_mem(*args) -> int:
        return f(*args)

    return make_generator(f_mem)

def make_generator_mem(f: Callable):
    @functools.cache
    def f_mem(*args) -> int:
        return f(*args)
    
    globals()[f.__name__] = f_mem

    return make_generator(f_mem)

def test_generator(gen):
    for i in gen:
        print(i)
        user_input = input()
        if user_input != "":
            return
        
def recfun(f):
    @functools.wraps(f)
    def _f(*a, **kwa): \
        return f(_f, *a, **kwa)
    return _f

@recfun
def fibonacci_self(self, n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    
    return self(n - 1) + self(n - 2)

def fibonacci_sys_eval(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    
    _f = eval(sys._getframe().f_code.co_name)
    
    return _f(n - 1) + _f(n - 2)
            
print("Squares:")
squares = make_generator(lambda x: x**2)   
test_generator(squares)
print("Fibonacci no mem:")
fibonacci_no_mem = make_generator(fibonacci)
test_generator(fibonacci_no_mem)
print("Fibonacci mem naive:")
fibonacci_mem_2 = make_generator_mem_naive(fibonacci_self)
test_generator(fibonacci_mem_2)
print("Fibonacci mem sys eval:")
fibonacci_mem_3 = make_generator_mem_naive(fibonacci_sys_eval)
test_generator(fibonacci_mem_3)
print("Fibonacci mem:")
fibonacci_mem = make_generator_mem(fibonacci)
test_generator(fibonacci_mem)