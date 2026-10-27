import numpy as np

# Q1:

temperature = np.array([25, 28, 31, 35, 38, 27, 33, 40])

# Q1 (A):

corrected_temperature = temperature + 2

print("Q1 (A) Corrected temperatures:")
print(corrected_temperature)

# Q1 (B):

fahrenheit = (9 / 5) * corrected_temperature + 32

print("\nQ1 (B) Temperatures in Fahrenheit:")
print(fahrenheit)

# Q1 (C):

readings_above_32 = corrected_temperature[corrected_temperature > 32]

print("\nQ1 (C) Readings greater than 32°C:")
print(readings_above_32)

# Q1 (D):

count_above_32 = np.sum(corrected_temperature > 32)

print("\nQ1 (D) Number of readings exceeding 32°C:")
print(count_above_32)

# Q1 (E):

print("\nQ1 (E) Explanation:")
print("Vectorization allows NumPy to perform operations on the")
print("entire array at once instead of explicitly iterating through")
print("each value. Boolean indexing allows us to select only the")
print("values satisfying a condition. These operations are faster,")
print("more concise, and generally more efficient than Python loops.")

# Q2:

steps = np.array([
    [5000, 6200, 7100],
    [8000, 7500, 9000],
    [4500, 5100, 4800],
    [9000, 8500, 9500]
])

# Q2 (A):

total_steps = np.sum(steps)

print("Q2 (A) Total steps recorded:")
print(total_steps)

# Q2 (B):

mean_steps = np.mean(steps)

print("\nQ2 (B) Mean number of steps:")
print(mean_steps)

# Q2 (C):

maximum_steps = np.max(steps)
minimum_steps = np.min(steps)

print("\nQ2 (C) Maximum steps:")
print(maximum_steps)

print("Q2 (C) Minimum steps:")
print(minimum_steps)

# Q2 (D):

daily_total = np.sum(steps, axis=0)

print("\nQ2 (D) Total steps for each day:")
print(daily_total)

# Q2 (E):

user_total = np.sum(steps, axis=1)

print("\nQ2 (E) Total steps for each user:")
print(user_total)

# Q2 (F):

max_position = np.argmax(steps)

user_index, day_index = np.unravel_index(max_position, steps.shape)

print("\nQ2 (F) Maximum step count:")
print(steps[user_index, day_index])

print("User:", user_index + 1)
print("Day:", day_index + 1)

# Q3 (A):

original = np.array([1, 2, 3, 4, 5, 6])

print("Q3 (A) Original array:")
print(original)

# Q3 (B):

subset = original[1:5]

print("\nQ3 (B) Subset:")
print(subset)

# Q3 (C):

subset[0] = 999

print("\nQ3 (C) Original after modifying subset:")
print(original)

print("Q3 (C) Subset:")
print(subset)

# Q3 (D):

copied_array = original[1:5].copy()

copied_array[0] = 500

print("\nQ3 (D) Original after modifying copied array:")
print(original)

print("Q3 (D) Copied array:")
print(copied_array)

# Q3 (E):

matrix = np.arange(1, 13).reshape(3, 4)

print("\nQ3 (E) 3 x 4 matrix:")
print(matrix)

# Q3 (F):

first_row = matrix[0, :]

last_row = matrix[-1, :]

second_column = matrix[:, 1]

selected_elements = matrix[1:3, 2:4]

print("\nQ3 (F) First row:")
print(first_row)

print("Q3 (F) Last row:")
print(last_row)

print("Q3 (F) Second column:")
print(second_column)

print("Q3 (F) Rows 1-2 and columns 2-3:")
print(selected_elements)

# Q3 (G):

flattened_array = matrix.flatten()
ravel_array = matrix.ravel()

print("\nQ3 (G) Using flatten():")
print(flattened_array)

print("Q3 (G) Using ravel():")
print(ravel_array)

# Q3 (H):

ravel_array[0] = 1000

print("\nQ3 (H) Ravel array after modification:")
print(ravel_array)

print("Q3 (H) Original matrix after modifying ravel:")
print(matrix)

# Q3 (I):

flattened_array[1] = 2000

print("\nQ3 (I) Flattened array after modification:")
print(flattened_array)

print("Q3 (I) Original matrix after modifying flatten:")
print(matrix)

# Q3 (J):

print("\nQ3 (J) Shape:")
print(matrix.shape)

print("Q3 (J) Number of dimensions:")
print(matrix.ndim)

print("Q3 (J) Number of elements:")
print(matrix.size)

print("Q3 (J) Data type:")
print(matrix.dtype)

# Q4 (A): 

X = np.array([
    [6, 70, 3],
    [5, 50, 6],
    [8, 80, 2],
    [4, 30, 8]
], dtype=float)

y = np.array([40, 65, 30, 85], dtype=float)

print("Q4 (A) Shape of X:", X.shape)
print("Q4 (A) Dimensions of X:", X.ndim)

# Q4 (B): 

X_T = X.T

print("\nQ4 (B) Transpose of X:")
print(X_T)


# Q4 (C):

XTX = X_T @ X

print("\nQ4 (C) X.T @ X:")
print(XTX)

# Q4 (D):

XTX_inverse = np.linalg.inv(XTX)

print("\nQ4 (D) Inverse of X.T @ X:")
print(XTX_inverse)

# Q4 (E):

beta = XTX_inverse @ X_T @ y

print("\nQ4 (E) OLS coefficients (beta):")
print(beta)

# Q4 (F):

print("\nQ4 (F) Coefficient interpretation:")
print("Sleep coefficient   :", beta[0])
print("Activity coefficient:", beta[1])
print("Stress coefficient  :", beta[2])

# Q4 (G):

new_user = np.array([5, 40, 7], dtype=float)

predicted_score = new_user @ beta

print("\nQ4 (G) New user:", new_user)
print("Q4 (G) Predicted assistance score:", predicted_score)