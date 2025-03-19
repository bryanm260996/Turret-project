from machine import Pin, I2C
import time
import math

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

    def desired_shooting(self, num_shots=3, current_threshold=2000, shot_delay=0.5, read_delay=0.01):
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

# Usage:
flywheel_controller = FlywheelController()
flywheel_controller.desired_shooting()
