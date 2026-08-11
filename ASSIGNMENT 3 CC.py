import pandas as pd

# QUESTION 1

data = {
    "Tid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Refund": ["Yes", "No", "No", "Yes", "No", "No", "Yes", "No", "No", "No"],
    "Marital Status": [
        "Single", "Married", "Single", "Married", "Divorced",
        "Married", "Divorced", "Single", "Married", "Single"
    ],
    "Taxable Income": [
        "125K", "100K", "70K", "120K", "95K",
        "60K", "220K", "85K", "75K", "90K"
    ],
    "Cheat": ["No", "No", "No", "No", "Yes", "No", "No", "Yes", "No", "Yes"]
}

df = pd.DataFrame(data)

print("\nQUESTION 1: Dataset")
print(df)

# QUESTION 2

print("\nQUESTION 2: Rows 0, 4, 7 and 8")
print(df.loc[[0, 4, 7, 8]])

# QUESTION 3

# Q3.1 - Select rows from index 3 to 7
print("\nQUESTION 3.1: Rows from index 3 to 7")
print(df.loc[3:7])


# Q3.2 - Select rows from index 4 to 8 and columns 2 to 4
print("\nQUESTION 3.2: Rows 4 to 8 and columns 2 to 4")
print(df.iloc[4:9, 2:5])


# Q3.3 - Select all rows with column index 1 to 3
print("\nQUESTION 3.3: All rows and columns 1 to 3")
print(df.iloc[:, 1:4])

# QUESTION 4

print("\nQUESTION 4: First five rows of Iris dataset")

iris_df = pd.read_csv("Dataset Assignment 3.csv")

print(iris_df.head())

# QUESTION 5

iris_df = iris_df.drop(index=4)

column_to_delete = iris_df.columns[3]
iris_df = iris_df.drop(columns=column_to_delete)

print("\nQUESTION 5: DataFrame after deleting row 4 and column 3")
print(iris_df)

# QUESTION 6

data = {
    "Employee_ID": [101, 102, 103, 104, 105],
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Edward"],
    "Department": ["HR", "IT", "IT", "Marketing", "Sales"],
    "Age": [29, 34, 41, 28, 38],
    "Salary": [50000, 70000, 65000, 55000, 60000],
    "Years_of_Experience": [4, 8, 10, 3, 12],
    "Joining_Date": [
        "2020-03-15",
        "2017-07-19",
        "2013-06-01",
        "2021-02-10",
        "2010-11-25"
    ],
    "Gender": ["Female", "Male", "Male", "Female", "Male"],
    "Bonus": [5000, 7000, 6000, 4500, 5000],
    "Rating": [4.5, 4.0, 3.8, 4.7, 3.5]
}

employees = pd.DataFrame(data)

print("\nQUESTION 6: Employee Dataset")
print(employees)

# Q6(a)

print("\nQ6(a): Shape of DataFrame")
print(employees.shape)

# Q6(b)

print("\nQ6(b): DataFrame Information")
employees.info()

# Q6(c)

print("\nQ6(c): Descriptive Statistics")
print(employees.describe())

# Q6(d)

print("\nQ6(d): First 5 Rows")
print(employees.head(5))

print("\nQ6(d): Last 3 Rows")
print(employees.tail(3))

# Q6(e)

# i. Average salary

average_salary = employees["Salary"].mean()
print("\nQ6(e)(i): Average Salary =", average_salary)

# ii. Total bonus

total_bonus = employees["Bonus"].sum()
print("Q6(e)(ii): Total Bonus =", total_bonus)

# iii. Youngest employee's age

youngest_age = employees["Age"].min()
print("Q6(e)(iii): Youngest Age =", youngest_age)

# iv. Highest performance rating

highest_rating = employees["Rating"].max()
print("Q6(e)(iv): Highest Performance Rating =", highest_rating)

# Q6(f)

employees_sorted = employees.sort_values(
    by="Salary",
    ascending=False
)

print("\nQ6(f): DataFrame Sorted by Salary (Descending)")
print(employees_sorted)

# Q6(g)

def categorize_rating(rating):
    if rating >= 4.5:
        return "Excellent"
    elif rating >= 4.0:
        return "Good"
    else:
        return "Average"


employees["Category"] = employees["Rating"].apply(categorize_rating)

print("\nQ6(g): Employee Categories")
print(employees[["Name", "Rating", "Category"]])

# Q6(h)

print("\nQ6(h): Missing Values")
print(employees.isnull().sum())

# Q6(i)

employees.rename(
    columns={"Employee_ID": "ID"},
    inplace=True
)

print("\nQ6(i): After Renaming Employee_ID to ID")
print(employees)

# Q6(j)

# i. More than 5 years of experience

experienced_employees = employees[
    employees["Years_of_Experience"] > 5
]

print("\nQ6(j)(i): Employees with more than 5 years of experience")
print(experienced_employees)


# ii. Employees belonging to IT department

it_employees = employees[
    employees["Department"] == "IT"
]

print("\nQ6(j)(ii): Employees in IT Department")
print(it_employees)

# Q6(k)

employees["Tax"] = employees["Salary"] * 0.10

print("\nQ6(k): DataFrame with Tax Column")
print(employees)

# Q6(l)

employees.to_csv(
    "employees_modified.csv",
    index=False
)

print("\nQ6(l): Modified DataFrame saved as employees_modified.csv")