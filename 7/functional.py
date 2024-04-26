from typing import List, Tuple, Dict, Any

'''
Nie wykorzystując imperatywnych instrukcji for, while, if , opracuj implementację każdej1
z poniższych funkcji:
a. Funkcja, która przyjmuje na wejściu listę ciągów znaków akronim zbudowany z
tych ciągów znaków. Przykład:
>>> acronym([“Zakład”, “Ubezpieczeń”, “Społecznych”])
ZUS
b. Funkcja, która przyjmuje na wejściu przyjmuje listę liczb i zwraca ich medianę.
Funkcja nie może korzystać z modułu statistics ani żadnego innego modułu do
obliczeń statystycznych. Przykład:
>>> median([1,1,19,2,3,4,4,5,1])
3
c. Funkcja obliczająca pierwiastek kwadratowy metodą Netwona. Funkcja
przyjmuje na wejściu pierwiastkowaną liczbę oraz epsilon i zwraca taki , żexy
i .y ≥ 0  |y2-x|<epsilon
Przykład:
1 Oileniezostanąużytewramachtzw.list/dictcomprehensionsluboperatoraternarnego.
1
>>> pierwiastek(3, epsilon = 0.1)
1.75
d. Funkcja, która przyjmuje na wejściu ciąg znaków, a zwraca na wyjściu słownik, w
którym kluczami są znaki występujące alfabetyczne występujące ciągu, a
wartościami listy słów zawierających te znaki. Przykład:
>>> make_alpha_dict(“on i ona”)
{'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}
e. Funkcja spłaszczająca listy. Funkcja powinna przyjmować listę, której
elementami mogą być elementy skalarne lub sekwencje. Spłaszczenie polega na
zmianie zagnieżdżonej struktury na jednowymiarową listę zawierającą wszystkie
elementy wewnętrznych sekwencji. Spłaszczenie powinno działać na wszystkich
poziomach zagnieżdżeń, tzn. wynikowa lista powinna zawierać tylko elementy
skalarne. Na potrzeby zadania należy przyjąć, że elementy skalarne to takie, które
nie są listami ani krotkami. Przykład:
>>> flatten([1, [2, 3], [[4, 5], 6]])
[1, 2, 3, 4, 5, 6]
'''

acronym = lambda x: ''.join([i[0] for i in x])

def acronym_fun(words: List[str], result=""):
    return result if not words else acronym_fun(words[1:], result + words[0][0]) 

def median(numbers: List[int]) -> int:
    numbers.sort()
    
    n = len(numbers)
    
    if n % 2 == 0:
        return (numbers[n // 2] + numbers[n // 2 - 1]) / 2
    return numbers[n // 2]

def functional_sort(numbers: List[int]) -> List[int]:
    if len(numbers) == 1:
        return numbers
    if len(numbers) == 0:
        return []
    head, tail = numbers[0], numbers[1:]
    return numbers if not numbers else functional_sort([x for x in tail if x < head]) + [head] + functional_sort([x for x in tail if x >= head])

def median_functionally(numbers: List[int]) -> int:
    numbers_sorted = functional_sort(numbers)
    
    n = len(numbers_sorted)
    
    if n % 2 == 0:
        return (numbers_sorted[n // 2] + numbers_sorted[n // 2 - 1]) / 2
    return numbers_sorted[n // 2] 

print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))

print(acronym_fun(["Zakład", "Ubezpieczeń", "Społecznych"]))

print(functional_sort([1,1,19,2,3,4,4,5,1]))

print(median_functionally([1,1,19,2,3,4,4,5,1]))

print(median([1,1,19,2,3,4,4,5,1])) 

'''
c. Funkcja obliczająca pierwiastek kwadratowy metodą Netwona. Funkcja
przyjmuje na wejściu pierwiastkowaną liczbę oraz epsilon i zwraca taki , żexy
i .y ≥ 0  |y2-x|<epsilon
Przykład:
1 Oileniezostanąużytewramachtzw.list/dictcomprehensionsluboperatoraternarnego.
1
>>> pierwiastek(3, epsilon = 0.1)
'''

def newton_sqrt(x: float, epsilon: float) -> float:
    def improve(guess: float) -> float:
        return (guess + x / guess) / 2

    def good_enough(guess: float) -> bool:
        return abs(guess ** 2 - x) < epsilon

    def sqrt_iter(guess: float) -> float:
        if good_enough(guess):
            return guess
        else:
            return sqrt_iter(improve(guess))

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

print(make_alpha_dict("on i ona"))

'''
Funkcja spłaszczająca listy. Funkcja powinna przyjmować listę, której
elementami mogą być elementy skalarne lub sekwencje. Spłaszczenie polega na
zmianie zagnieżdżonej struktury na jednowymiarową listę zawierającą wszystkie
elementy wewnętrznych sekwencji. Spłaszczenie powinno działać na wszystkich
poziomach zagnieżdżeń, tzn. wynikowa lista powinna zawierać tylko elementy
skalarne. Na potrzeby zadania należy przyjąć, że elementy skalarne to takie, które
nie są listami ani krotkami. Przykład:
>>> flatten([1, [2, 3], [[4, 5], 6]])
[1, 2, 3, 4, 5, 6]
'''

def flatten(elements: List[Any]) -> List[Any]:
    def aux(elements: List[Any], result: List[Any]):
        if len(elements) == 0:
            return result
        head, tail = elements[0], elements[1:]
        if isinstance(head, list):
            return aux(head + tail, result)
        else:
            return aux(tail, result + [head])
        
    return aux(elements, [])

print(flatten([1, [2, 3], [[4, 5], 6]]))