import random
from collections import Counter

# QUESTION 1

roll_number = input("Enter your 8-digit roll number: ")

# Validate roll number
if not roll_number.isdigit() or len(roll_number) != 8:
    raise ValueError("Please enter exactly 8 digits.")

# Extract digits and multiply each digit by 10
L = [int(digit) * 10 for digit in roll_number]

print("\nQUESTION 1: List L")
print(L)

# Q1(i)

print("\nQ1(i): Original List")
print(L)

# Q1(ii)

L.append(100)
print("\nQ1(ii) - After append(100):")
print(L)

L.insert(2, 50)
print("\nQ1(ii) - After insert(50) at index 2:")
print(L)

# Q1(iii)

# remove() removes the first occurrence of a specified value.
L.remove(100)
print("\nQ1(iii) - After remove(100):")
print(L)

# pop() removes and returns an element using its index.
removed_element = L.pop(2)
print("\nQ1(iii) - After pop(2):")
print(L)
print("Element removed using pop():", removed_element)

# Q1(iv)

L.sort()
print("\nQ1(iv): Ascending Order")
print(L)

L.sort(reverse=True)
print("\nQ1(iv): Descending Order")
print(L)

# Q1(v)

print("\nQ1(v): First three elements")
print(L[:3])

print("Q1(v): Last three elements")
print(L[-3:])

# Q1(vi)

average_L = sum(L) / len(L)

greater_than_average = [
    value for value in L
    if value > average_L
]

print("\nQ1(vi): Average of L =", average_L)
print("Elements greater than average:")
print(greater_than_average)

# QUESTION 2

scores = tuple(L[:8])

print("\nQUESTION 2: Tuple scores")
print(scores)

# Q2(i)

highest_score = max(scores)
highest_index = scores.index(highest_score)

lowest_score = min(scores)
lowest_count = scores.count(lowest_score)

print("\nQ2(i): Highest score =", highest_score)
print("Index of highest score =", highest_index)
print("Lowest score =", lowest_score)
print("Number of times lowest score appears =", lowest_count)

# Q2(ii)

reversed_scores = list(reversed(scores))

print("\nQ2(ii): Reversed tuple as a list")
print(reversed_scores)

# Q2(iii)

search_score = int(input("\nQ2(iii): Enter a score to search: "))

if search_score in scores:
    print("First occurrence index =", scores.index(search_score))
else:
    print("Score not present")

# Q2(iv)

try:
    scores[0] = 100

except TypeError as error:
    print("\nQ2(iv): TypeError occurred")
    print("Tuples are immutable and cannot be changed directly.")

# Q2(v)

first_score, second_score, *remaining_scores = scores

print("\nQ2(v): Tuple Unpacking")
print("First score:", first_score)
print("Second score:", second_score)
print("Remaining scores:", remaining_scores)

# QUESTION 3

random.seed(int(roll_number))

random_numbers = [
    random.randint(100, 900)
    for _ in range(100)
]

print("\nQUESTION 3: Random Numbers")
print(random_numbers)

# Q3(i)

print("\nQ3(i): 100 Random Numbers")
print(random_numbers)

# Q3(ii)

odd_numbers = [
    number for number in random_numbers
    if number % 2 != 0
]

print("\nQ3(ii): Odd Numbers")
print(odd_numbers)
print("Count of odd numbers:", len(odd_numbers))

# Q3(iii)

even_numbers = [
    number for number in random_numbers
    if number % 2 == 0
]

print("\nQ3(iii): Even Numbers")
print(even_numbers)
print("Count of even numbers:", len(even_numbers))

# Q3(iv)

def is_prime(number):
    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


prime_numbers = [
    number for number in random_numbers
    if is_prime(number)
]

print("\nQ3(iv): Prime Numbers")
print(prime_numbers)
print("Count of prime numbers:", len(prime_numbers))

# Q3(v)

frequency = Counter(random_numbers)

most_frequent_number, frequency_count = frequency.most_common(1)[0]

print("\nQ3(v): Most Frequent Number")
print("Number:", most_frequent_number)
print("Number of occurrences:", frequency_count)

# QUESTION 4

digits = [int(digit) for digit in roll_number]

A = {digit * 7 for digit in digits}
B = {digit * 9 for digit in digits}

print("\nQUESTION 4: Sets")
print("Set A =", A)
print("Set B =", B)

# Q4(i)

union_AB = A.union(B)

print("\nQ4(vi): Union of A and B")
print(union_AB)

# Q4(ii)

intersection_AB = A.intersection(B)

print("\nQ4(vii): Intersection of A and B")
print(intersection_AB)

# Q4(iii)

A_minus_B = A.difference(B)
B_minus_A = B.difference(A)

print("\nQ4(viii): A - B")
print(A_minus_B)

print("Q4(viii): B - A")
print(B_minus_A)

# Q4(iv)

symmetric_difference = A.symmetric_difference(B)

print("\nQ4(ix): Symmetric Difference")
print(symmetric_difference)

# Q4(v)

print("\nQ4(x): Subset and Superset Check")

print("Is A a subset of B?", A.issubset(B))
print("Is B a superset of A?", B.issuperset(A))

# Q4(vi)

value = int(input("\nQ4(xi): Enter a value to remove from A: "))

A.discard(value)

print("Set A after discard():")
print(A)

# QUESTION 5

my_dict = {
    "name": "<your name>",
    "roll_no": "<your roll number>",
    "branch": "<your branch>",
    "age": "<your age>",
    "city": "<your home city>"
}

print("\nOriginal Dictionary:")
print(my_dict)

# Q5(i)

my_dict["location"] = my_dict.pop("city")

print("\nQ5(i): After renaming city to location")
print(my_dict)

# Q5(ii)

my_dict["cgpa"] = 7.96

print("\nQ5(ii): After adding CGPA")
print(my_dict)

# Q5(iii)

my_dict["age"] = int(input("\nEnter your current age: "))

my_dict["age"] += 1

print("\nQ5(iii): After increasing age by 1")
print(my_dict)

# Q5(iv)

# Create two separate copies
dict_pop = my_dict.copy()
dict_del = my_dict.copy()


# Method 1: Using pop()
removed_branch = dict_pop.pop("branch")

print("\nQ5(iv): Using pop()")
print("Removed value:", removed_branch)
print("Dictionary after pop():")
print(dict_pop)


# Method 2: Using del
del dict_del["branch"]

print("\nQ5(iv): Using del")
print("Dictionary after del:")
print(dict_del)

# Q5(v)

print("\nQ5(v): Key-Value Pairs")

for key, value in my_dict.items():
    print(f"{key} -> {value}")

# Q5(vi)

print("\nQ5(vi): Checking for email key")

if "email" in my_dict:
    print("Email:", my_dict["email"])
else:
    print("Email key is not present in the dictionary.")

# Q5(vii)

dict2 = {
    "name": "Rahul Sharma",
    "roll_no": "10234567",
    "branch": "ECE",
    "age": 21,
    "city": "Mumbai"
}

merged_dict = {**my_dict, **dict2}

print("\nQ5(vii): Second Dictionary")
print(dict2)

print("\nMerged Dictionary:")
print(merged_dict)

print(
    "\nQ5(vii) Explanation: "
    "When the same key exists in both dictionaries, "
    "the value from the second dictionary overwrites "
    "the value from the first dictionary."
)

# Q5(viii)

string_values_dict = {
    key: value
    for key, value in my_dict.items()
    if isinstance(value, str)
}

print("\nQ5(viii): Dictionary containing only string values")
print(string_values_dict)