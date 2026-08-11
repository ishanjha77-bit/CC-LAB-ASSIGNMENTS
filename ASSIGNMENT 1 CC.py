#QUESTION 1.1

for i in range(1,4):
    print("Ishan")

#QUESTION 2.1

a = input("Enter a number: ")
b = input("Enter another number: ")
c = input("Enter a third number: ")

d = int(a) + int(b) + int(c)
print("The sum is:", d)

#QUESTION 2.2

e = input("Enter a string: ")
f = input("Enter another string: ")
g = input("Enter a third string: ")

h = e + " " + f + " " + g
print("The concatenated string is:", h)

#QUESTION 4.1

s = 7

for i in range(1, 11):
    s = 7 * i
    print("Table of 7 is -->", s)

s = 9

for i in range(1, 11):
    s = 9 * i
    print("Table of 9 is -->", s)

#QUESTION 4.2

s = int(input("Enter a number to print its table: "))

for i in range(1, 11):
    d = s * i
    print("Table of", s, "is -->", d)


#QUESTION 4.3

s = int(input("Enter a number : "))

d = 0

for i in range(1, s + 1):
    d = d + i

print("The sum of numbers from 1 to", s, "is", d)

#QUESTION 5.1

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
c = int(input("Enter third number: "))

maximum = max(a, b, c)

print("Maximum number is:", maximum)

#QUESTION 5.2

n = int(input("Enter the value of n: "))

total = 0

for i in range(1, n + 1):
    if i % 7 == 0 and i % 9 == 0:
        total = total + i

print("Sum =", total)

#QUESTION 5.3

n = int(input("Enter the value of n: "))

total = 0

for i in range(2, n + 1):
    prime = True

    for j in range(2, i):
        if i % j == 0:
            prime = False
            break

    if prime:
        total = total + i

print("Sum of prime numbers =", total)

#QUESTION 6.1

n = int(input("Enter a number: "))

def sum_odd(n):
    total = 0

    for i in range(1, n + 1):
        if i % 2 != 0:
            total = total + i

    return total

print("Sum of odd numbers =", sum_odd(n))

#QUESTION 6.2

n = int(input("Enter a number: "))

def sum_prime(n):
    total = 0

    for i in range(2, n + 1):
        prime = True

        for j in range(2, i):
            if i % j == 0:
                prime = False
                break

        if prime:
            total = total + i

    return total

print("Sum of prime numbers =", sum_prime(n))