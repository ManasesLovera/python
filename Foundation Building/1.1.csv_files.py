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