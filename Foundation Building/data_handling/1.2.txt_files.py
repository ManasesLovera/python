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

Extend Project 2: Ignore common stop words like "the," "is," "a," etc., from counting.
"""

from collections import Counter

# Define common stop words to exclude
stop_words = {"the", "is", "a", "an", "and", "of", "to", "in", "on", "for", "with"}

# Read file and split words
with open("1.2.example.txt", "r") as file:
    content = file.read()
    words = content.lower().split()

# Filter out stop words
filtered_words = [word for word in words if word not in stop_words]

# Count word occurences
word_counts = Counter(filtered_words)
for word, count in word_counts.items():
    print(f"{word}: {count}")