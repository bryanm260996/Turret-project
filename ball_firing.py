from machine import Pin, I2C
import time
import math

INA260_ADDRESS = 0x40
INA260_CURRENT_REGISTER = 0x01

ina260_i2c = I2C(0, scl=Pin(1), sda=Pin(0))


# Define GPIO pins for the flywheels
flywheel_PIN = Pin(15, Pin.OUT)
loader_pin = Pin(14, Pin.OUT)


def read_current():
    """Read current from INA260."""
    try:
        data = ina260_i2c.readfrom_mem(INA260_ADDRESS, INA260_CURRENT_REGISTER, 2)
        raw_current = int.from_bytes(data, 'big')
        if raw_current & 0x8000:
            raw_current -= 1 << 16
        current_ma = raw_current * 1.25  # Convert to mA
        return current_ma
    except OSError:
        print("Error reading INA260.")
        return math.nan  # Return nan if read fails

def desired_shooting():
    flywheel_PIN.value(1)
    time.sleep(2)
    loader_pin.value(1)
    num_shots = 3
    balls_shot = 0
    while balls_shot != num_shots:
        current = read_current()
        #print(f"Current: {current} mA")
        time.sleep(0.01)  # Delay for 0.01 seconds (10 milliseconds) before reading again
        
        if current > 2000:
            loader_pin.value(0)
            balls_shot = balls_shot + 1
            time.sleep(0.5)        # Wait for 0.5 seconds
            loader_pin.value(1)
            print(f"{balls_shot}")

    loader_pin.value(0)    
    flywheel_PIN.value(0)     
        
    
desired_shooting()  
