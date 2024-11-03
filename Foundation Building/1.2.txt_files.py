# Reading from a Text File:
with open("1.2.example.txt", "r") as file:
    content = file.read()
    print(content)

# Writing to a Text File:
with open("1.2.output.txt", "w") as file:
    file.write("Hello, World!\nThis is a sample text file.")

# Appending to a Text File:
with open("1.2.output.txt", "a") as file:
    file.write("\nAdding another line to the file.")


# Project 2: Text File Organizer

"""
Objective: Read a text file with sentences and count the occurrences of each word.
"""

from collections import Counter

with open("1.2.example.txt", "r") as file:
    content = file.read()
    words = content.lower().split()

word_counts = Counter(words)
for word, count in word_counts.items():
    print(f"{word}: {count}")