import random
from typing import List

'''
Skonstruuj klasę PasswordGenerator, która będzie obsługiwać protokół iteratora.
Iterator powinien zwracać kolejne losowo generowane hasła. Iterator powinien mieć
następujące metody:
a. __init__(self, length, charset, count): funkcja inicjująca iterator z
2 parametrami:
i. długością hasła oraz
ii. zestawem znaków, z których losowo będą tworzone hasła (domyślnie
wszystkie litery alfabetu oraz cyfry),
iii. maksymalną liczbą haseł do wygenerowania.
b. __iter__(self): metoda zwracająca iterator
c. __next__(self): metoda zwracająca kolejne losowo wygenerowane hasło.
Po wygenerowaniu self.count haseł, podnieś wyjątek StopIteration.
Przetestuj iterator wywołując jawnie wbudowaną funkcję next() oraz w ramach
pętli for.
'''

class PasswordGenerator:
    def __init__(self, *args):
        self.length: int = args[0]
        if isinstance(args[1], List):
            self.charset: List[str] = args[1]
            self.count: int = args[2]
        elif isinstance(args[1], int):
            self.charset: List[str] = PasswordGenerator.default_charset()            
            self.count: int = args[1]
        self.generated = 0
        
    @staticmethod
    def default_charset():
        return list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration
        self.generated += 1
        return ''.join(random.choices(self.charset, k=self.length))
    
if __name__ == "__main__":    
    password_generator_1 = PasswordGenerator(5, 3)
    password_generator_2 = PasswordGenerator(10, ["a", "b", "c"], 3)
    
    print("using next()")
    while True:
        try:
            print(next(password_generator_1))
        except StopIteration:
            break
        
    print()
    print("for loop")
    
    for password in password_generator_2:
        print(password)
    