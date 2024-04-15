import math
from pylx16a.lx16a import LX16A, ServoTimeoutError
import time

# Initialization and servo setup
LX16A.initialize("COM8", 0.1)

try:
    # Initialize servos
    servo1 = LX16A(1)
    servo10 = LX16A(10)
    servo3 = LX16A(3)
    servo30 = LX16A(30)
    servo2 = LX16A(2)
    servo20 = LX16A(20)
    servo4 = LX16A(4)
    servo40 = LX16A(40)

    # Set angle limits for all servos
    servo1.set_angle_limits(0, 240)
    servo10.set_angle_limits(0, 240)
    servo3.set_angle_limits(0, 240)
    servo30.set_angle_limits(0, 240)
    servo2.set_angle_limits(0, 240)
    servo20.set_angle_limits(0, 240)
    servo4.set_angle_limits(0, 240)
    servo40.set_angle_limits(0, 240)
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

# Initial positions for all servos
initial_positions = {
    1: 66.72, 10: 132, 3: 140.88, 30: 72,
    2: 108.96, 20: 140.88, 4: 88.8, 40: 136.80
}

# Move all servos to initial position
for servo_id, position in initial_positions.items():
    eval(f'servo{servo_id}').move(position)
time.sleep(1)
print("Homing Complete")

# Initialize control variables
t = 0
t2 = 0
first_loop_active = False
second_loop_active = False

# Main control loop
while True:
    if not second_loop_active:
        # First loop for servos 1, 10, 3, and 30
        while t <= math.pi:
            servo1.move(math.cos(t+0.3) * 10 + initial_positions[1])
            servo10.move(math.sin(t+math.pi+0.3) * 30 + initial_positions[10])
            servo3.move(math.cos(t+0.3) * 10 + initial_positions[3])
            servo30.move(math.sin(t+0.3) * 45 + initial_positions[30])

            time.sleep(0.05)
            t += 0.1

            # Trigger second loop at 30% of the first loop
            if t > (math.pi * 0.3):
                second_loop_active = True
                t2 = 0  # Reset t2 for the second loop

        # Reset first set to home positions
        servo1.move(initial_positions[1])
        servo10.move(initial_positions[10])
        servo3.move(initial_positions[3])
        servo30.move(initial_positions[30])
        print("Moved to Home 1")
        first_loop_active = False
        t = 0

    if second_loop_active:
        # Second loop for servos 2, 20, 4, and 40
        while t2 <= math.pi:
            servo2.move(math.cos(t2+0.3) * 13 + initial_positions[2])
            servo20.move(math.sin(t2+0.3) * 30 + initial_positions[20])
            servo4.move(math.cos(t2+0.3) * 13 + initial_positions[4])
            servo40.move(math.sin(t2+math.pi+0.3) * 45 + initial_positions[40])

            time.sleep(0.05)
            t2 += 0.1

            # Trigger first loop at 30% of the second loop
            if t2 > (math.pi * 0.3):
                first_loop_active = True
                t = 0  # Reset t for the first loop

        # Reset second set to home positions
        servo2.move(initial_positions[2])
        servo20.move(initial_positions[20])
        servo4.move(initial_positions[4])
        servo40.move(initial_positions[40])
        print("Moved to Home 2")
        second_loop_active = False
        t2 = 0
