import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Function to read data from a text file with a single number per line
def read_single_column_data(filename):
    y = []
    with open(filename, 'r') as file:
        for line in file:
            y.append(float(line.strip()))
    return y


# Read data from the file once
# Testfill data.txt
filename = '201m (0).txt'
y_data = read_single_column_data(filename)

# Initialize the plot
fig, ax = plt.subplots()
x, y = [], []
line, = ax.plot(x, y, marker='o')

# Number of data points to display
window_size = 300


# Update function for animation
def update(frame):
    if frame < len(y_data):
        x.append(frame)
        y.append(y_data[frame])

        # Trim data if it exceeds window size
        if len(x) > window_size:
            x.pop(0)
            y.pop(0)

    # Update the line data
    line.set_data(x, y)

    # Adjust the limits of the plot if needed
    ax.relim()
    ax.autoscale_view()

    return line,


# Create an animation
ani = animation.FuncAnimation(fig, update, frames=len(y_data), interval=1, repeat=False)

# Add a title and labels
plt.title('Real-Time Data from Single Column File')
plt.xlabel('Index')
plt.ylabel('y values')

# Show the plot
plt.show()