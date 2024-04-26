from functional import *

def test_functional_sort():
    # Test case with an empty list
    numbers = []
    assert functional_sort(numbers) == []

    # Test case with a single element
    numbers = [5]
    assert functional_sort(numbers) == [5]

    # Test case with already sorted list
    numbers = [1, 2, 3, 4, 5]
    assert functional_sort(numbers) == [1, 2, 3, 4, 5]

    # Test case with reverse sorted list
    numbers = [5, 4, 3, 2, 1]
    assert functional_sort(numbers) == [1, 2, 3, 4, 5]

    # Test case with unsorted list
    numbers = [3, 1, 4, 2, 5]
    assert functional_sort(numbers) == [1, 2, 3, 4, 5]

    # Test case with duplicate elements
    numbers = [3, 1, 4, 2, 5, 3, 2]
    assert functional_sort(numbers) == [1, 2, 2, 3, 3, 4, 5]

    print("All test cases pass")

test_functional_sort()