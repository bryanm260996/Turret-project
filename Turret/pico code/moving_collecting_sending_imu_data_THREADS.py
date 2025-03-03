import machine
import time
import threading
from moving_functions import MovingTurret
from bno055 import *
import ttyacm

# Initialize comms
tty = ttyacm.open(1)

# Initialize turret
turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)

def get_gyro_data(imu):
    """
    Reads gyroscope data (x, y, z) from the IMU and prints them.
    """
    gyro_data = imu.gyro()
    if gyro_data:
        print(f'Gyro X: {gyro_data[0]:4.2f} Y: {gyro_data[1]:4.2f}  Z: {gyro_data[2]:4.2f}')
    return gyro_data


def get_euler_data(imu):
    """
    Reads Euler angles (yaw, pitch, roll) from the IMU and prints them.
    """
    euler_data = imu.euler()
    if euler_data:
        print(f'Euler Yaw: {euler_data[0]:4.2f}  Pitch: {euler_data[1]:4.2f}  Roll: {euler_data[2]:4.2f}')
    return euler_data


def imu_data_loop(imu):
    """
    Continuously read gyroscope and Euler data and send them over tty separately.
    """
    while True:
        gyro_data = get_gyro_data(imu)
        if gyro_data:
            gyro_x, gyro_y, gyro_z = gyro_data[0], gyro_data[1], gyro_data[2]
            timestamp = time.time()
            print(f"Sending Gyro Data: Time:{timestamp} X={gyro_x}, Y={gyro_y}")
            tty.print(f'{timestamp},{gyro_x},{gyro_y}\n')

        #euler_data = get_euler_data(imu)
        #if euler_data:
        #    yaw, pitch, roll = euler_data[0], euler_data[1], euler_data[2]
        #    timestamp = time.time()
        #    print(f"Sending Euler Data: Time:{timestamp} Yaw={yaw}, Pitch={pitch}, Roll={roll}")
        #    tty.print(f'EULER,{timestamp},{yaw},{pitch},{roll}\n')

        time.sleep(0.1)  # Adjust the sleep time as needed


def command_input_loop():
    """
    Handles user input to control the turret.
    """
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


def main_loop():
    """
    Main control loop to manage turret movement and IMU data reading.
    """
    try:
        # Initialize IMU
        i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
        imu = BNO055(i2c)


        # Start IMU data collection in a separate thread
        imu_thread = threading.Thread(target=imu_data_loop, args=(imu,))
        imu_thread.daemon = True  # Ensures the thread exits when the main program exits
        imu_thread.start()

        # Start user input loop
        command_input_loop()

    except KeyboardInterrupt:
        print("\nFinalizing program...")
        turret.stop()  # Ensure turret motors stop safely
        print("Program terminated.")


# Run the main loop
main_loop()
