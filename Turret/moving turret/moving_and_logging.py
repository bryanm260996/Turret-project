import machine
import time
from moving_functions import MovingTurret
from accelerometer_function import accelerometer_data
from bno055 import *



file= 'yaw_and_pitch_data.txt'
file_work= open(file, 'a')

# Initialize turret and IMU
turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)

def get_accelerometer_data(imu):
    """
    Reads Euler angles (yaw, pitch) from the IMU and prints them.
    """
    euler_data = imu.euler()
    if euler_data:
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
            
            if euler_data:
                yaw, pitch = euler_data[0], euler_data[2]
                # Add logic to adjust turret movement based on the IMU data if needed
                print(f"Processing IMU data: Yaw={yaw}, Pitch={pitch}")
                file_work.write(f'yaw:{yaw}, pitch:{pitch}')
                file_work.flush()



    except KeyboardInterrupt:
        print("\nFinalizing program...")
        turret.stop()  # Ensure turret motors stop safely
        print("Program terminated.")

# Run the main loop
main_loop()
file_work.close()

