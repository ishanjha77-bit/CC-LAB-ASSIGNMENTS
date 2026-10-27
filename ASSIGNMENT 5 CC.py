import numpy as np

# Q1. NumPy 1-D Array and Basic Operations

# Create a NumPy 1-D array with 5 elements
arr = np.array([10, 20, 30, 40, 50])

print("\n================ Q1 ================")
print("Original Array:", arr)

# a) Addition of 2 to all elements
addition = arr + 2
print("After adding 2:", addition)

# b) Multiply all elements by 3
multiplication = arr * 3
print("After multiplying by 3:", multiplication)

# c) Divide every element by 2
division = arr / 2
print("After dividing by 2:", division)

# Q2. Basic NumPy Array Operations

print("\n================ Q2 ================")

# ------------------------------------------------------------
# Q2(a) Reverse the NumPy array

arr = np.array([1, 2, 3, 6, 4, 5])

print("\nQ2(a)")
print("Original Array:", arr)

# [::-1] reverses the array
reversed_arr = arr[::-1]

print("Reversed Array:", reversed_arr)

# Q2(b) Find the most frequent value and its indices


print("\nQ2(b)")

# Array x
x = np.array([1, 2, 3, 4, 5, 1, 2, 1, 1, 1])

# np.unique() returns:
# values  -> unique values
# counts  -> number of occurrences of each value
values, counts = np.unique(x, return_counts=True)

# Find the index of the maximum frequency
most_frequent_index = np.argmax(counts)

# Get the most frequent value
most_frequent_value = values[most_frequent_index]

# Find all indices where the value occurs
indices = np.where(x == most_frequent_value)[0]

print("Array x:", x)
print("Most frequent value:", most_frequent_value)
print("Frequency:", counts[most_frequent_index])
print("Indices:", indices)

# Find most frequent value for array y

y = np.array([1, 1, 1, 2, 3, 4, 2, 4, 3, 3])

values_y, counts_y = np.unique(y, return_counts=True)

most_frequent_index_y = np.argmax(counts_y)
most_frequent_value_y = values_y[most_frequent_index_y]

indices_y = np.where(y == most_frequent_value_y)[0]

print("\nArray y:", y)
print("Most frequent value:", most_frequent_value_y)
print("Frequency:", counts_y[most_frequent_index_y])
print("Indices:", indices_y)

# Q3. Access Elements of a 2-D NumPy Array

print("\n================ Q3 ================")

# Create the given 2-D array
arr_2d = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("2-D Array:")
print(arr_2d)

# Q3(a) 

element_1 = arr_2d[0, 1]

print("\nQ3(a)")
print("1st row, 2nd column:", element_1)

# Q3(b)

element_2 = arr_2d[2, 0]

print("\nQ3(b)")
print("3rd row, 1st column:", element_2)

# Q4. 

print("\n================ Q4 ================")

Ishan = np.linspace(10, 100, 25)

print("Array:")
print(Ishan)

# Dimensions of the array
print("\nNumber of dimensions:", Ishan.ndim)

# Shape of the array
print("Shape:", Ishan.shape)

# Total number of elements
print("Total number of elements:", Ishan.size)

# Data type of each element
print("Data type:", Ishan.dtype)

# Total number of bytes consumed
print("Total bytes consumed:", Ishan.nbytes)

# Q4 - Transpose

Ishan_2d = Ishan.reshape(5, 5)

print("\n5 x 5 Array:")
print(Ishan_2d)

# Transpose using reshape()
transposed_array = Ishan_2d.reshape(5, 5).T

print("\nTranspose using reshape():")
print(transposed_array)

# Transpose using T attribute
transposed_using_T = Ishan_2d.T

print("\nTranspose using T attribute:")
print(transposed_using_T)

# Yes, both methods give the same result.
print("\nAre both transpose results same?",
      np.array_equal(transposed_array, transposed_using_T))

# Q5.

print("\n================ Q5 ================")

# Create the 3 x 4 array as given in the assignment
ucs420_Ishan = np.array([
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 15, 20, 35]
])

print("Original Array (ucs420_Ishan):")
print(ucs420_Ishan)

mean_value = np.mean(ucs420_Ishan)

print("\nMean:", mean_value)

median_value = np.median(ucs420_Ishan)

print("Median:", median_value)

max_value = np.max(ucs420_Ishan)

print("Maximum:", max_value)

min_value = np.min(ucs420_Ishan)

print("Minimum:", min_value)

unique_elements = np.unique(ucs420_Ishan)

print("Unique Elements:", unique_elements)

reshaped_ucs420_Ishan = ucs420_Ishan.reshape(4, 3)

print("\nReshaped Array (4 x 3):")
print(reshaped_ucs420_Ishan)

resized_ucs420_Ishan = np.resize(ucs420_Ishan, (2, 3))

print("\nResized Array (2 x 3):")
print(resized_ucs420_Ishan)