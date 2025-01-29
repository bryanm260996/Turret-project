from bno055 import *
import time

def accelerometer_data():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))  
    imu = BNO055(i2c)
    calibrated = False
    while True:
        if not calibrated:
            calibrated = imu.calibrated()
    
    # Continuously read euler data
        euler_data = imu.euler()
        print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
        time.sleep(0.5)
        
accelerometer_data()
        
        
