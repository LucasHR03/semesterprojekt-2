import matplotlib.pyplot as plt

# Function to read data from a text file
def read_single_column_data(filename):
    y = []
    with open(filename, 'r') as file:
        for line in file:
            y.append(float(line.strip()))
    return y

# Read data from the file
# forsøgsfil data.txt
filename = '201m (0).txt'
y = read_single_column_data(filename)

# Generate x values as a sequence of integers
x = list(range(len(y)))

# Create the plot
plt.plot(x, y, marker='o')

# Add a title and labels
plt.title('Data from Single Column File')
plt.xlabel('Index')
plt.ylabel('y values')

# Show the plot
plt.show()
