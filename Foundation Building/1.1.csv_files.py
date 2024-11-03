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
"""
total_grade = 0
count = 0

with open('1.1.students.csv','r') as file:
    reader = csv.reader(file)
    next(reader) # Skip header row
    for row in reader:
        name, grade = row
        total_grade += int(grade)
        count += 1

average_grade = total_grade / count
print('Average grade:', average_grade)