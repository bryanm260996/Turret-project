import time
import machine
from bno055 import *

def accelerometer_data():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))  
    imu = BNO055(i2c)
    calibrated = False
    
    try:
        while True:
            # Wait until the IMU is calibrated
            if not calibrated:
                calibrated = imu.calibrated()
                if calibrated:
                    print("IMU is calibrated.")
            
            # Continuously read euler data
            try:
                euler_data = imu.euler()
                print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
            except Exception as e:
                print(f"Error reading euler data: {e}")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("Exiting accelerometer data collection.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function (this would be in your main script, not inside this file directly)
# accelerometer_data()
