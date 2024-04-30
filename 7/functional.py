from typing import List, Dict, Any

acronym = lambda x: ''.join([i[0] for i in x])

def acronym_fun(words: List[str], result=""):
    return result if not words else acronym_fun(words[1:], result + words[0][0]) 

def median(numbers: List[int]) -> int|float:
    numbers.sort()
    
    n = len(numbers)
    
    return (numbers[n // 2] + numbers[n // 2 - 1]) / 2 if n % 2 == 0 else numbers[n // 2]

def functional_sort(numbers: List[int]) -> List[int]:    
    return [] if len(numbers) == 0 \
    else numbers if not numbers \
    else functional_sort([x for x in numbers[1:] if x < numbers[0]]) + [numbers[0]] + functional_sort([x for x in numbers[1:] if x >= numbers[0]])

def median_functionally(numbers: List[int]) -> int|float:
    numbers_sorted = functional_sort(numbers)
    
    n = len(numbers_sorted)
    
    return (numbers_sorted[n // 2] + numbers_sorted[n // 2 - 1]) / 2 if n % 2 == 0 else numbers_sorted[n // 2] 

def newton_sqrt(x: float, epsilon: float) -> float:
    def improve(guess: float) -> float:
        return (guess + x / guess) / 2

    def good_enough(guess: float) -> bool:
        return abs(guess ** 2 - x) < epsilon

    def sqrt_iter(guess: float) -> float:
        return guess if good_enough(guess) else sqrt_iter(improve(guess))

    return sqrt_iter(1.0)

print(newton_sqrt(3, epsilon=0.1))
        
def analyze_word(word: str, chars: List[str], dictionary: Dict[str, List[str]]):
    if len(chars) == 0:
        return dictionary
    
    char, tail = chars[0], chars[1:]
    
    if char.isalpha():
        if char in dictionary:
            dictionary[char].append(word)
        else:
            dictionary[char] = [word]
    return analyze_word(word, tail, dictionary)

def make_alpha_dict(string: str) -> Dict[str, List[str]]:
    def aux(words: List[str], dictionary: Dict[str, List[str]]):
        if len(words) == 0:
            return dictionary
        word, tail = words[0], words[1:] if len(words) > 1 else []
        
        analyze_word(word, list(word), dictionary)
                
        return aux(tail, dictionary)
        
    words = string.split()
    return aux(words, {})

def flatten(elements: List[Any]) -> List[Any]:
    def aux(elements: List[Any], result: List[Any]):
        if len(elements) == 0:
            return result
        head, tail = elements[0], elements[1:]
        return aux(head + tail, result) if isinstance(head, list) else aux(tail, result + [head])
        
    return aux(elements, [])

print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))

print(acronym_fun(["Zakład", "Ubezpieczeń", "Społecznych"]))

print(functional_sort([1,1,19,2,3,4,4,5,1]))

print(median_functionally([1,1,19,2,3,4,4,5,1]))

print(median([1,1,19,2,3,4,4,5,1])) 

print(make_alpha_dict("on i ona"))

print(flatten([1, [2, 3], [[4, 5], 6]]))