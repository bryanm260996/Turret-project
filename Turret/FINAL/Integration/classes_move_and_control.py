from machine import PWM, Pin, I2C
import time
from bno055 import BNO055

# Initialize I2C and IMU
i2c = I2C(1, sda=Pin(2), scl=Pin(3))  
imu = BNO055(i2c)

# Class to move turret
class MovingTurret:
    def __init__(self, pan_pin_1, pan_pin_2, tilt_pin_1, tilt_pin_2):
        self.pan_servo = PWM(Pin(pan_pin_1))
        self.pan_servo2 = PWM(Pin(pan_pin_2))
        self.pan_servo.freq(50)
        self.pan_servo2.freq(50)

        self.tilt_servo = PWM(Pin(tilt_pin_1))
        self.tilt_servo2 = PWM(Pin(tilt_pin_2))
        self.tilt_servo.freq(50)
        self.tilt_servo2.freq(50)

    def set_speed(self, pwm1, pwm2, speed):
        speed = max(min(speed, 1.0), -1.0)  # Clamp speed
        if speed > 0:
            pwm1.duty_u16(int(speed * 65535))
            pwm2.duty_u16(0)
        elif speed < 0:
            pwm2.duty_u16(int(-speed * 65535))
            pwm1.duty_u16(0)
        else:
            pwm1.duty_u16(0)
            pwm2.duty_u16(0)

    def move_turret(self, pan_speed, tilt_speed):
        self.set_speed(self.pan_servo, self.pan_servo2, pan_speed)
        self.set_speed(self.tilt_servo, self.tilt_servo2, tilt_speed)

# Controller class
class Controller:
    def __init__(self, turret, imu):
        self.turret = turret
        self.imu = imu

    def get_imu_data(self):
        try:
            euler_data = self.imu.euler()
            if euler_data and None not in euler_data:
                yaw = euler_data[0]
                pitch = euler_data[1]
                return yaw, pitch
            else:
                return None, None
        except Exception as e:
            print(f"Error reading IMU: {e}")
            return None, None

    def move_to_position(self, desired_yaw, desired_pitch, k_p=0.012):
        while True:
            current_yaw, current_pitch = self.get_imu_data()
            
            if current_yaw is None or current_pitch is None:
                print("IMU data unavailable. Retrying...")
                time.sleep(0.1)
                continue  # Skip iteration if IMU data is invalid
            if current_yaw >180:
                current_yaw= abs(current_yaw-360)
                
            
            yaw_error = desired_yaw - current_yaw
            pitch_error = desired_pitch - current_pitch
            print(f"Current Yaw: {current_yaw:.2f}, Yaw Error: {yaw_error:.2f}")
            print(f"Current Pitch: {current_pitch:.2f}, Pitch Error: {pitch_error:.2f}")
            
            pan_speed = k_p * yaw_error
            tilt_speed = k_p * pitch_error

            pan_speed = max(min(pan_speed, 1.0), -1.0)
            tilt_speed = max(min(tilt_speed, 1.0), -1.0)

            self.turret.move_turret(pan_speed, tilt_speed)
            
            if abs(yaw_error) < 0.1 and abs(pitch_error) < 0.1:
                self.turret.move_turret(0, 0)
                break
            
            time.sleep(0.1)

# Initialize the turret
turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)  

# Create a Controller instance
controller = Controller(turret, imu)

# Move turret to target position
controller.move_to_position(desired_yaw=40, desired_pitch=-20)
print(yaw)
print("Turret reached target position!")
