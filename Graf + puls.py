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
# Testfile data.txt
filename = '201m (0).txt'
y_data = read_single_column_data(filename)

# Initialize the plot
fig, ax = plt.subplots()
x, y = [], []
line, = ax.plot(x, y)
counter_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

# Number of data points to display
window_size = 300

# Counter for data points above the threshold
threshold_count = 0

# Threshold value
threshold = 0.006

# Frame number when the count was last incremented
last_increment = 0

# Update function for animation
def update(frame):
    global threshold_count, last_increment

    # Increment the counter if the current frame is above the threshold
    if frame < len(y_data) and y_data[frame] > threshold:
        # Check if the current frame is more than 50 frames away from the last increment frame
        if frame - last_increment >= 50:
            threshold_count += 1
            counter_text.set_text(f'Count: {threshold_count}')
            print(f"Data point {frame}: {y_data[frame]} is above the threshold. Count: {threshold_count}")
            last_increment = frame

    # Update the plot with the current data point
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

    return line, counter_text


# Create an animation
ani = animation.FuncAnimation(fig, update, frames=len(y_data), interval=0.5, repeat=False)

plt.title('Real-Time Data from Single Column File')
plt.xlabel('Index')
plt.ylabel('y values')

# Show the plot
plt.show()
