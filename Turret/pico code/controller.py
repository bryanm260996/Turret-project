import machine
import time
from bno055 import BNO055

# Controller parameters
desired_pos = 0  # Desired position in degrees (e.g., yaw angle)
desired_vel = 0  # Desired velocity (e.g., degrees per second)

kp = 10  # Proportional gain
ki = 5   # Integral gain

# Initialize the IMU
i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))  
imu = BNO055(i2c)

# Function to calculate error
def calculate_error(actual_pos, actual_vel):
    yaw_error = desired_yaw_pos - actual_yaw_pos
    yaw_error_dot = desired_yaw_vel - actual_yaw_vel
    pitch_error = desired_pitch_pos - actual_pitch_pos
    pitch_error_dot = desired_pitch_vel - actual_pitch_vel
    return yaw_error, yaw_error_dot, pitch_error, pitch_error_dot

# Controller function
def controller(error, error_dot):
    duty_cycle = kp * error + ki * error_dot
    return duty_cycle

# Function to get IMU data
def get_imu_data(imu):
    try:
        euler_data = imu.euler()
        gyro_data = imu.gyro()

        if euler_data and None not in euler_data and gyro_data and None not in gyro_data:
            yaw = euler_data[0]
            pitch = euler_data[1]
            yaw_rate = gyro_data[0]
            pitch_rate = gyro_data[1]
            return (yaw, pitch), (yaw_rate, pitch_rate)
        else:
            print("No data available")
            return (None, None), (None, None)
    except Exception as e:
        print(f"Error reading IMU data: {e}")
        return (None, None), (None, None)

# Main loop
while True:
    desired_yaw_pos=input('enter desired yaw position')
    desired_pitch_pos=input('enter desired pitch position')
    desired_yaw_vel=input('enter desired yaw velocity')
    desired_pitch_vel=input('enter desired pitch velocity')
    
    (yaw_and_pitch, yaw_and_pitch_rates) = get_imu_data(imu)

# Extract individual values
    yaw_actual, pitch_actual = yaw_and_pitch
    yaw_rate_actual, pitch_rate_actual = yaw_and_pitch_rates

#actual_values
    actual_yaw_pos = yaw_actual
    actual_pitch_pos = pitch_actual
    actual_yaw_vel = yaw_rate_actual
    actual_pitch_vel = pitch_rate_actual
    
#calculating error
    yaw_error = desired_yaw_pos - actual_yaw_pos
    yaw_error_dot = desired_yaw_vel - actual_yaw_vel
    pitch_error = desired_pitch_pos - actual_pitch_pos
    pitch_error_dot = desired_pitch_vel - actual_pitch_vel
# controllers
   duty_cycle_yaw = kp * yaw_error + ki * yaw_error_dot
   duty_cycle_pitch = kp * pitch_error + ki * pitch_error_dot



