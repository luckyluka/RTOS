import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import re

# Configure your COM port and baudrate
ser = serial.Serial("COM6", 115200, timeout=1)

# Buffers for three tasks
task1_data = deque(maxlen=200)
task2_data = deque(maxlen=200)
task3_data = deque(maxlen=200)

# Regex to parse STM32 output: "task1:123"
pattern = re.compile(r"(task[123]):(\d+)")

def update(frame):
    line = ser.readline().decode(errors='ignore').strip()
    match = pattern.match(line)
    if match:
        task_name, value = match.groups()
        value = int(value)
        if task_name == "task1":
            task1_data.append(value)
        elif task_name == "task2":
            task2_data.append(value)
        elif task_name == "task3":
            task3_data.append(value)

    # Plot all three tasks
    plt.cla()
    plt.plot(task1_data, label="task1")
    plt.plot(task2_data, label="task2")
    plt.plot(task3_data, label="task3")
    plt.legend()
    plt.xlabel("Sample")
    plt.ylabel("Value")
    plt.title("STM32 Task Execution Output")

ani = animation.FuncAnimation(plt.gcf(), update, interval=50)
plt.show()
