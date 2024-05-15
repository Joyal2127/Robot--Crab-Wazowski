import sys
import re
import time
from datetime import datetime, timedelta
from collections import deque
import threading
import subprocess
import atexit
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Global variables
current_process = None
data_window = deque()
angles = []
COLLISION_THRESHOLD = 1000  # Collision threshold in millimeters

def parse_log_line(line):
    """
    Parse a line of LiDAR data to extract angle, distance, and intensity.
    """
    pattern = r'angle:(\d+\.\d+),distance\(mm\):(\d+),intensity:(\d+)'
    match = re.search(pattern, line)
    if match:
        distance = int(match.group(2))
        if 100 <= distance <= 8000:
            angle = float(match.group(1)) * np.pi / 180  # Convert to radians
            angles.append((angle, distance))
            return {
                'angle': angle,
                'distance': distance,
                'intensity': int(match.group(3)),
                'timestamp': datetime.now()
            }
    return None

def direction_algorithm(batch):
    """
    Determine the best direction to move based on the LiDAR data.
    """
    forward_zone = list(range(330, 361)) + list(range(0, 30))
    left_zone = list(range(225, 330))
    right_zone = list(range(30, 135))

    zone_distances = {'forward': 0, 'left': 0, 'right': 0}
    zone_weights = {'forward': 0, 'left': 0, 'right': 0}

    for entry in batch:
        angle = entry['angle']
        distance = entry['distance']
        weight = 1.5 if 340 <= angle <= 360 or 0 <= angle <= 20 else 1.0

        if angle in forward_zone:
            zone_distances['forward'] += distance * weight
            zone_weights['forward'] += weight
        elif angle in left_zone:
            zone_distances['left'] += distance * weight
            zone_weights['left'] += weight
        elif angle in right_zone:
            zone_distances['right'] += distance * weight
            zone_weights['right'] += weight

    zone_averages = {zone: (zone_distances[zone] / zone_weights[zone] if zone_weights[zone] != 0 else 0)
                     for zone in ['forward', 'left', 'right']}
    direction = max(zone_averages, key=zone_averages.get)
    return 'stop' if zone_averages[direction] == 0 else direction

def start_process(script_name):
    """
    Start a new process and terminate the old one if it exists.
    """
    global current_process
    if current_process is not None:
        current_process.terminate()
        current_process.wait()
    current_process = subprocess.Popen(['/usr/bin/python3', script_name])

def clean_up():
    """
    Ensure all processes are terminated when the script exits.
    """
    global current_process
    if current_process is not None:
        current_process.terminate()
        current_process.wait()

atexit.register(clean_up)

def update_plot(frame):
    """
    Update the plot with new angle data.
    """
    plt.cla()
    ax = plt.subplot(1, 1, 1, polar=True)
    collision_angles, collision_distances = zip(*[(a, d) for a, d in angles if d < COLLISION_THRESHOLD])
    ax.scatter(collision_angles, collision_distances, color='red')  # Collision points in red
    ax.set_ylim(0, COLLISION_THRESHOLD)  # Set radius limits
    ax.set_title('LiDAR Collision Detection')
    non_collision_angles, non_collision_distances = zip(*[(a, d) for a, d in angles if d >= COLLISION_THRESHOLD])
    ax.scatter(non_collision_angles, non_collision_distances)  # Non-collision points

def process_input():
    """
    Process input data continuously and manage directional decisions.
    """
    global current_process, data_window
    next_decision_time = datetime.now() + timedelta(seconds=3)
    last_decision = None

    # Start the real-time LiDAR plot in a background thread
    threading.Thread(target=lambda: FuncAnimation(plt.gcf(), update_plot, interval=1000).start(), daemon=True).start()
    
    while True:
        line = sys.stdin.readline().strip()
        if line:
            data = parse_log_line(line)
            if data:
                data_window.append(data)
                while data_window and (datetime.now() - data_window[0]['timestamp']).total_seconds() > 3:
                    data_window.popleft()

        if datetime.now() >= next_decision_time:
            if data_window:
                decision = direction_algorithm(list(data_window))
                print(f"Decision: {decision}")
                if decision != last_decision:
                    if decision == 'forward':
                        start_process('/home/skynet/straight.py')
                    elif decision == 'left':
                        start_process('/home/skynet/left.py')
                    elif decision == 'right':
                        start_process('/home/skynet/right.py')
                    elif decision == 'stop':
                        start_process('/home/skynet/march.py')
                    last_decision = decision
            next_decision_time += timedelta(seconds=3)

if __name__ == "__main__":
    # Setup the plot for real-time LiDAR visualization
    plt.ion()
    plt.show()

    # Run the process input logic
    process_input()
