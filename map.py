import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math
import subprocess
import re

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 10))
scat = ax.scatter([], [], c='red')
robot_dot, = ax.plot(0, 0, 'bo')  # Robot position in blue
ax.axis('equal')
ax.grid(True)

# Regular expression pattern for parsing LiDAR data
pattern = re.compile(r'angle:(\d+\.\d+),distance\(mm\):(\d+),intensity:(\d+)')

def update(frame):
    line = process.stdout.readline()
    match = pattern.search(line)
    if match:
        angle = float(match.group(1))
        distance = float(match.group(2))
        x = distance * math.cos(math.radians(angle))
        y = distance * math.sin(math.radians(angle))
        scat.set_offsets(np.c_[x, y])
    return scat, robot_dot

# Start the LiDAR data generation subprocess
process = subprocess.Popen(['./startnode2.sh', 'LD19', 'serial', 'ttyUSB1'], stdout=subprocess.PIPE, text=True)

# Create the animation
ani = animation.FuncAnimation(fig, update, interval=50, blit=True)

plt.show()
