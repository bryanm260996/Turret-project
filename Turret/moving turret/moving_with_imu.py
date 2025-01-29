from moving_functions import MovingTurret
from accelerometer_function import *
import time
from bno055 import *

# IMU connection
i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))  
imu = BNO055(i2c)
calibrated = False

# Create an instance of the MovingTurret class
turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)

# Infinite loop to move the turret in all directions
while True:
    if not calibrated:
        calibrated = imu.calibrated()
    
    # Continuously read euler data
    euler_data = imu.euler()
    print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
    
    # Move the turret in all directions and update position data
    turret.pan_right()  # Move pan motor to the right
    time.sleep(0.5)  # Wait for 1.5 seconds    
    euler_data = imu.euler()  # Read position data after moving
    print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
    
    turret.pan_left()   # Move pan motor to the left
    time.sleep(1.5)  # Wait for 1.5 seconds
    euler_data = imu.euler()  # Read position data after moving
    print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
    
    turret.tilt_up()    # Tilt the turret upwards
    time.sleep(0.5)  # Wait for 1.5 seconds
    euler_data = imu.euler()  # Read position data after moving
    print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
    
    turret.tilt_down()  # Tilt the turret downwards
    time.sleep(0.5)  # Wait for 1.5 seconds
    euler_data = imu.euler()  # Read position data after moving
    print(f'Heading {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
