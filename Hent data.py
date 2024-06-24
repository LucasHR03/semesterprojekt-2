import csv
import os

# Get the current working directory
path = os.getcwd()

# Specify the file name
file_name = '201m (0).txt'

# Construct the full path to the file
file_A = os.path.join(path, file_name)

def read_file(file_A, delimiter=',', chunk_size=100000):

    data = []
    with open(file_A, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=delimiter)
        List = []
        for i, row in enumerate(reader):
            List.append(row)
            if (i + 1) % chunk_size == 0:
                data.extend(List)
                List = []  # Clear the List
        if List:  # Add the last List if it's not empty
            data.extend(List)
    return data

# Read the file
data = read_file(file_A)
# Print the first 10 rows
for row in data[:100]:
    print(row)
