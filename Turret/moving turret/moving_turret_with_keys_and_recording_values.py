from moving_functions import MovingTurret
from accelerometer_function import *
import time
import machine
from bno055 import *

# Initialize turret and IMU
turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)

def get_accelerometer_data(imu):
    """
    Reads Euler angles (yaw, pitch) from the IMU and prints them.
    """
    euler_data = imu.euler()
    print(f'Yaw {euler_data[0]:4.0f}  Pitch {euler_data[2]:4.0f}')
    return euler_data

def main_loop():
    """
    Main control loop to manage turret movement and accelerometer data reading.
    """
    try:
        # Initialize IMU
        i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
        imu = BNO055(i2c)

        while True:
            command = input("Enter command: ").strip().lower()
            if command == 'a':
                turret.pan_left()
            elif command == 'd':
                turret.pan_right()
            elif command == 'w':
                turret.tilt_up()
            elif command == 's':
                turret.tilt_down()
            elif command == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid command. Use 'a', 'd', 'w', 's', or 'q'.")

            
            # Get and display accelerometer data
            euler_data = get_accelerometer_data(imu)
            
            # Add logic to adjust turret movement based on the IMU data if needed
            if euler_data:
                yaw, pitch = euler_data[0], euler_data[2]


    except KeyboardInterrupt:
        print("\nFinalizing program...")
        turret.stop()  # Ensure turret motors stop safely
        print("Program terminated.")

# Run the main loop
main_loop()
