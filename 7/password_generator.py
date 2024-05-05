import random
from typing import List

class PasswordGenerator:
    def __init__(self, length: int, *args):
        self.length: int = length
                
        if isinstance(args[0], List):
            self.charset: List[str] = args[0]
            self.count: int = args[1]
        elif isinstance(args[0], int):
            self.charset = PasswordGenerator.default_charset()            
            self.count = args[0]
        else:
            raise ValueError("Invalid arguments: needs a list of characters or an integer as the second argument.")
        
        self.validate_charset()
        
        self.generated = 0
        
    def validate_charset(self):
        for char in self.charset:
            if len(char) != 1:
                raise ValueError("Invalid character in charset: " + char)
        
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
    password_generator_2 = PasswordGenerator(10, list("abc"), 3)
    
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
    