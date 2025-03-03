from machine import PWM, Pin
import time
from bno055 import BNO055

# Define GPIO pins for the pan motor
PAN_PIN_1 = 9  
PAN_PIN_2 = 10

# Define GPIO pins for the tilt motor
TILT_PIN_1 = 12
TILT_PIN_2 = 13

# Initialize the PWM objects for the pan motor
pan_servo = PWM(Pin(PAN_PIN_1))
pan_servo2 = PWM(Pin(PAN_PIN_2))
pan_servo.freq(50)
pan_servo2.freq(50)

# Initialize the PWM objects for the tilt motor
tilt_servo = PWM(Pin(TILT_PIN_1))
tilt_servo2 = PWM(Pin(TILT_PIN_2))
tilt_servo.freq(50)
tilt_servo2.freq(50)

# Controller parameters
kp = 200  # Proportional gain
ki = 150   # Integral gain

# Initialize the IMU
i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))  
imu = BNO055(i2c)

# Function to set the speed of a motor
def set_speed(pwm1, pwm2, speed):
    speed = max(min(speed, 1.0), -1.0)  # Clamp speed between -1.0 and 1.0
    if speed > 0:
        pwm1.duty_u16(int(speed * 3500))
        pwm2.duty_u16(0)
    elif speed < 0:
        pwm2.duty_u16(int(-speed * 3500))
        pwm1.duty_u16(0)
    else:
        pwm1.duty_u16(0)
        pwm2.duty_u16(0)

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
    desired_yaw_pos = float(input('Enter desired yaw position: '))
    desired_pitch_pos = float(input('Enter desired pitch position: '))
    desired_yaw_vel = float(input('Enter desired yaw velocity: '))
    desired_pitch_vel = float(input('Enter desired pitch velocity: '))
    
    (yaw_and_pitch, yaw_and_pitch_rates) = get_imu_data(imu)
    yaw_actual, pitch_actual = yaw_and_pitch
    yaw_rate_actual, pitch_rate_actual = yaw_and_pitch_rates

    if yaw_actual is not None and pitch_actual is not None:
        # Calculate errors
        yaw_error = desired_yaw_pos - yaw_actual
        yaw_error_dot = desired_yaw_vel - yaw_rate_actual
        pitch_error = desired_pitch_pos - pitch_actual
        pitch_error_dot = desired_pitch_vel - pitch_rate_actual

        # Calculate duty cycles using PID controller
        duty_cycle_yaw = kp * yaw_error + ki * yaw_error_dot
        duty_cycle_pitch = kp * pitch_error + ki * pitch_error_dot

        # Set motor speeds based on duty cycle
        set_speed(pan_servo, pan_servo2, duty_cycle_yaw)
        set_speed(tilt_servo, tilt_servo2, duty_cycle_pitch)

    time.sleep(0.1)
