import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import serial
import time
import sqlite3

# Adjust the serial port and baud rate to match your Arduino settings
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

# Define chunk size
CHUNK_SIZE = 300

# Queue to hold EKG-data
data_queue = queue.Queue()


# Function to read data from Arduino and save to the database in chunks
def read_from_arduino(serial_port, baud_rate, data_queue):
    conn = sqlite3.connect('SP2database.db')  # Connect to the database in the current directory
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ekg_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL
        )
    ''')
    conn.commit()

    data_chunk = []  # List to store data chunk

    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for the connection to initialize

        print("Connected to Arduino on port:", serial_port)

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                try:
                    value = float(line)
                    data_queue.put(value)
                    data_chunk.append(value)

                    if len(data_chunk) >= CHUNK_SIZE:
                        cursor.executemany('INSERT INTO ekg_data (value) VALUES (?)', [(val,) for val in data_chunk])
                        conn.commit()
                        print(f"Inserted chunk: {data_chunk}")
                        data_chunk.clear()  # Clear the chunk after saving
                except ValueError:
                    print(f"Invalid data: {line}")

    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        if data_chunk:
            cursor.executemany('INSERT INTO ekg_data (value) VALUES (?)', [(val,) for val in data_chunk])
            conn.commit()
            print(f"Inserted final chunk: {data_chunk}")
        ser.close()
        conn.close()
        print("Connection closed.")


# Initialize global variables
window_size = 300
threshold = 0.006
above_threshold_count = 0
last_increment_frame = 50
y_data = []


# Function to create the plot window
def create_plot_window():
    global window_size, threshold, above_threshold_count, last_increment_frame, y_data

    # Initialize the plot and the text annotation
    fig, ax = plt.subplots()
    x, y = [], []
    line, = ax.plot(x, y)
    counter_text = ax.text(0.02, 0.95, f'Count: {above_threshold_count}', transform=ax.transAxes, fontsize=12,
                           verticalalignment='top')

    # Update function for animation
    def update(frame):
        global above_threshold_count, last_increment_frame, y_data

        conn = sqlite3.connect('SP2database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM ekg_data ORDER BY id DESC LIMIT ?', (window_size,))
        rows = cursor.fetchall()
        conn.close()

        y_data = [row[0] for row in rows][::-1]  # Reverse to maintain order
        x_data = list(range(len(y_data)))

        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()

        above_threshold_count = sum(1 for value in y_data if value > threshold)
        counter_text.set_text(f'Count: {above_threshold_count}')
        return line, counter_text

    # Create an animation
    ani = animation.FuncAnimation(fig, update, interval=50, repeat=False, cache_frame_data=False)

    # Add a title and labels
    plt.title('Real-Time EKG')
    plt.xlabel('Index')
    plt.ylabel('y values')

    # Show the plot
    plt.show()


# Function to start the plot animation
def start_plot():
    global window_size, threshold, above_threshold_count, last_increment_frame, y_data

    # Get the user inputs
    try:
        window_size = int(window_size_entry.get())
        threshold = float(threshold_entry.get())
        above_threshold_count = 0
        last_increment_frame = 50  # Reset counter
        y_data = []
        create_plot_window()
    except ValueError:
        messagebox.showerror("Error", "Invalid input for window size or threshold.")


if __name__ == "__main__":
    # Initialize the main Tkinter window
    root = tk.Tk()
    root.title("EKG")

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

    # Start the thread for reading data from Arduino
    read_thread = threading.Thread(target=read_from_arduino, args=(SERIAL_PORT, BAUD_RATE, data_queue))
    read_thread.start()

    # Start the Tkinter main loop
    root.mainloop()

    # Wait for the read_thread to finish
    read_thread.join()
