from machine import PWM, Pin, I2C
import time
from bno055 import BNO055
import math

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

    def move_to_position(self, desired_yaw, desired_pitch, k_p=0.012, timeout=3):
        start_time = time.time()  # Record the start time
        while True:
            current_yaw, current_pitch = self.get_imu_data()
            
            # Check timeout
            if time.time() - start_time > timeout:
                print("Timeout reached while moving to position.")
                self.turret.move_turret(0, 0)  # Stop the turret
                break

            if current_yaw is None or current_pitch is None:
                print("IMU data unavailable. Retrying...")
                time.sleep(0.1)
                continue  # Skip iteration if IMU data is invalid
                
            if current_yaw > 180:
                current_yaw = abs(current_yaw - 360)

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
                print("Target position reached!")
                self.turret.move_turret(0, 0)
                break
            
            time.sleep(0.1)
            
#class to shoot

class FlywheelController:
    INA260_ADDRESS = 0x40
    INA260_CURRENT_REGISTER = 0x01

    def __init__(self, i2c_scl_pin=1, i2c_sda_pin=0, flywheel_pin=15, loader_pin=14):
        # Initialize I2C and pins
        self.ina260_i2c = I2C(0, scl=Pin(i2c_scl_pin), sda=Pin(i2c_sda_pin))
        self.flywheel_pin = Pin(flywheel_pin, Pin.OUT)
        self.loader_pin = Pin(loader_pin, Pin.OUT)

    def read_current(self):
        """Read current from INA260."""
        try:
            data = self.ina260_i2c.readfrom_mem(self.INA260_ADDRESS, self.INA260_CURRENT_REGISTER, 2)
            raw_current = int.from_bytes(data, 'big')
            if raw_current & 0x8000:
                raw_current -= 1 << 16
            current_ma = raw_current * 1.25  # Convert to mA
            return current_ma
        except OSError:
            print("Error reading INA260.")
            return math.nan  # Return nan if read fails

    def desired_shooting(self, num_shots=2, current_threshold=2000, shot_delay=0.5, read_delay=0.01):
        """Perform the shooting action."""
        self.flywheel_pin.value(1)
        time.sleep(2)
        self.loader_pin.value(1)
        balls_shot = 0

        while balls_shot < num_shots:
            current = self.read_current()
            #print(f"Current: {current} mA")
            time.sleep(read_delay)  # Delay before reading again
            
            if current > current_threshold:
                self.loader_pin.value(0)
                balls_shot += 1
                time.sleep(shot_delay)  # Wait for 0.5 seconds between shots
                self.loader_pin.value(1)
                print(f"{balls_shot}")

        self.loader_pin.value(0)
        self.flywheel_pin.value(0)



# Define target positions (fake targets)
target_positions = [
    {"yaw": 40, "pitch": -10},  # Target 1
    {"yaw": 60, "pitch": -5}  # Target 2
]
## Create instances

flywheel_controller = FlywheelController()
# Initialize the turret
turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)  
# Create a Controller instance
controller = Controller(turret, imu)


# Loop through each target position
for target in target_positions:
    # Move to the target position
    print(f"Moving to target position: Yaw={target['yaw']}, Pitch={target['pitch']}")
    controller.move_to_position(desired_yaw=target["yaw"], desired_pitch=target["pitch"])
    print("Turret reached target position!")

    # Trigger the shooting mechanism
    print("Shooting...")
    flywheel_controller.desired_shooting()
    print("Shooting completed!")

print("All targets completed!")

