import math
from pylx16a.lx16a import LX16A, ServoTimeoutError
import time

# Initialization and servo setup
LX16A.initialize("COM11", 0.1)

try:
    # Initialize servos
    servo1 = LX16A(1)
    servo10 = LX16A(10)
    servo3 = LX16A(3)
    servo30 = LX16A(30)
    servo2 = LX16A(2)
    servo20 = LX16A(20)
    servo4 = LX16A(4)
    print("Servo 4 initialized")
    servo40 = LX16A(40)
    print("Servo 40 initialized")
    servo1.set_angle_limits(0, 240)
    servo2.set_angle_limits(0, 240)
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

# Move servos to initial positions
servo1.move(66.72) 
servo10.move(132)
servo3.move(140.88)
servo30.move(72)
servo2.move(108.96)
servo20.move(140.88)
servo4.move(88.8)
servo40.move(136.80)
time.sleep(1)  
print("Homing Complete")   

loop_counter = 0  # Initialize counter for the loop

while loop_counter < 3:
    t = 0
    while t <= math.pi:
        servo1.move(math.cos(t+0.3) * 10 + 66.72)
        servo10.move(math.sin(t+0.3) * 30 + 132)
        servo3.move(math.cos(t+0.3) * 10 + 140.88)
        servo30.move(math.sin(t+0.3) * 45 + 72)
        time.sleep(0.05)  
        t += 0.1  
    servo1.move(66.72)
    servo3.move(140.88)
    print("Moved to Home 1")
    
    t = 0
    while t <= math.pi:
        servo2.move(math.cos(t+0.3) * 13 + 108.96)
        servo20.move(math.sin(t+0.3) * 30 + 140.88)
        servo4.move(math.cos(t+0.3) * 13 + 88.8)
        servo40.move(math.sin(t+0.3) * 45 + 136.80)
        
        time.sleep(0.05)
        t += 0.1
    
    servo2.move(108.96)
    servo4.move(88.8)
    print("Moved to Home 2")
    
    loop_counter += 1  # Increment the loop counter

print("Completed 3 full rotations")
