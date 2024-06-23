import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk, messagebox


# Read data from text file
def read_single_column_data(filename):
    y = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                y.append(float(line.strip()))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
    return y


# Read data from the file once
filename = '201m (0).txt'
y_data = read_single_column_data(filename)

# Number of data points to display
window_size = 300

# Counter for data points above the threshold
above_threshold_count = 0

# Threshold value
threshold = 0.006

# Frame number when the count was last incremented
last_increment_frame = 50


# Function to create the plot window
def create_plot_window():
    global y_data, window_size, threshold, above_threshold_count, last_increment_frame

    # Initialize the plot and the text annotation
    fig, ax = plt.subplots()
    x, y = [], []
    line, = ax.plot(x, y)
    counter_text = ax.text(0.02, 0.95, f'Count: {above_threshold_count}', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    # Update function for animation
    def update(frame):
        global above_threshold_count, last_increment_frame

        # Increment the counter if the current frame is above the threshold
        if frame < len(y_data) and y_data[frame] > threshold:
            # Check if the current frame is more than 50 frames away from the last increment frame
            if frame - last_increment_frame >= 50:
                above_threshold_count += 1
                last_increment_frame = frame

        # Update the counter text
        counter_text.set_text(f'Count: {above_threshold_count}')

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
    ani = animation.FuncAnimation(fig, update, frames=len(y_data), interval=50, repeat=False)

    # Add a title and labels
    plt.title('Real-Time EKG')
    plt.xlabel('Index')
    plt.ylabel('y values')

    # Show the plot
    plt.show()


# Function to start the plot animation
def start_plot():
    global window_size, threshold, above_threshold_count, last_increment_frame

    # Get the user inputs
    try:
        window_size = int(window_size_entry.get())
        threshold = float(threshold_entry.get())
        above_threshold_count = 0
        last_increment_frame = 50  # Reset counter
        if not y_data:
            messagebox.showwarning("Warning", "No data loaded.")
            return
        create_plot_window()
    except ValueError:
        messagebox.showerror("Error", "Invalid input for window size or threshold.")


# Initialize the main Tkinter window
root = tk.Tk()
root.title("EKG")

# Initialize global variables
window_size = 300
threshold = 0.006
above_threshold_count = 0
last_increment_frame = 50

# Create and place widgets in the Tkinter window
window_size_label = ttk.Label(root, text="Window Size:")
window_size_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

window_size_entry = ttk.Entry(root)
window_size_entry.insert(0, "300")
window_size_entry.grid(row=0, column=1, padx=10, pady=10)

threshold_label = ttk.Label(root, text="Threshold:")
threshold_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

threshold_entry = ttk.Entry(root)
threshold_entry.insert(0, "0.006")
threshold_entry.grid(row=1, column=1, padx=10, pady=10)

start_button = ttk.Button(root, text="Start Plot", command=start_plot)
start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

# Start the Tkinter main loop
root.mainloop()
