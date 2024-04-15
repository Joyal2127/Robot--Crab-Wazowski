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
    # Additional initialization code here
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

servo1.move(66.72) 
servo10.move(168)
servo3.move(140.88)
servo30.move(108.96)
servo2.move(108.96)
servo20.move(109.92)
servo4.move(88.8)
servo40.move(103.92)
#print("Homing Routine one complete")
#print("Moving up")
servo1.move(21.84) 
servo2.move(63.60) 
servo3.move(103.20) 
servo4.move(42.96)
print("Moved up")
time.sleep(2)
#return to normal Position
servo1.move(66.72) 
servo10.move(132)
servo3.move(140.88)
servo30.move(72)
servo2.move(108.96)
servo20.move(140.88)
servo4.move(88.8)
servo40.move(136.80)
print("Homing Complete")
 