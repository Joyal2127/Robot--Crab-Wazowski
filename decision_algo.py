import sys
import re
import time
from collections import deque
from datetime import datetime, timedelta

def parse_log_line(line):
    """
    Parse a line of LiDAR data.
    Expects data in the format:
    [LDS][INFO][timestamp][stamp:timestamp,angle:angle,distance(mm):distance,intensity:intensity]
    Returns a dictionary with angle, distance, and intensity if parsing is successful and within the specified range.
    """
    pattern = r'angle:(\d+\.\d+),distance\(mm\):(\d+),intensity:(\d+)'
    match = re.search(pattern, line)
    if match:
        distance = int(match.group(2))
        if 100 <= distance <= 8000: 
            return {
                'angle': float(match.group(1)),
                'distance': distance,
                'intensity': int(match.group(3)),
                'timestamp': datetime.now()  # Capture the time when the data was processed
            }
    return None

def direction_algorithm(batch):
    """
    Determine movement direction based on the weighted average distance of parsed LiDAR data in each zone.
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

def process_input():
    data_window = deque()
    next_decision_time = datetime.now() + timedelta(seconds=3)  # Update to 3 seconds

    while True:
        line = sys.stdin.readline().strip()
        if line:
            data = parse_log_line(line)
            if data:
                data_window.append(data)
                # Clean old data
                while data_window and (datetime.now() - data_window[0]['timestamp']).total_seconds() > 3:  # Changed to 3 seconds
                    data_window.popleft()

        if datetime.now() >= next_decision_time:
            if data_window:
                decision = direction_algorithm(list(data_window))
                print(f"Decision: {decision}")
            next_decision_time += timedelta(seconds=3)  # Schedule next decision for 3 seconds later

if __name__ == "__main__":
    process_input()
