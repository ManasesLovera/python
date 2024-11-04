import csv

# Reading from a CSV file
with open("1.1.sample.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Chicago"],
    ["Charlie", 35, "San Francisco"]
]

with open("1.1.output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Project 1: Simple CSV Data Processor

"""
Objective: Read a CSV file containing a list of students with names and grades, then calculate the average grade.

Modify Project 1: Add functionality to find the highest and lowest grades.
"""
total_grade = 0
count = 0
highest_grade = float('-inf')
lowest_grade = float('inf')
highest_student = ""
lowest_student = ""

with open('1.1.students.csv','r') as file:
    reader = csv.reader(file)
    next(reader) # Skip header row

    for row in reader:
        name, grade = row
        grade = int(grade)
        total_grade += grade
        count += 1

        if grade > highest_grade:
            highest_grade = grade
            highest_student = name

        if grade < lowest_grade:
            lowest_grade = grade
            lowest_student = name

average_grade = total_grade / count
print('Average grade:', average_grade)
print(f"Highest = Student: {highest_student}, Grade: {highest_grade}")
print(f"Lowest = Student: {lowest_student}, Grade: {lowest_grade}")