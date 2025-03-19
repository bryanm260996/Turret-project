from machine import Pin
import time

# Define GPIO pins for the flywheels
flywheel_PIN = Pin(15, Pin.OUT)
loader_pin = Pin(14, Pin.OUT)

# Function to activate motors
def activate_motors(ball_number):
    for i in range(ball_number):
        flywheel_PIN.value(1)  # Flywheel runs continuously
        time.sleep(2)          # Flywheel runs for 2 seconds

        loader_pin.value(1)    # Loader runs for 0.5 seconds
        time.sleep(0.1)        # Wait for 0.5 seconds
        loader_pin.value(0)    # Turn off the loader
        flywheel_PIN.value(0)  # Turn off the flywheel
        time.sleep(0.5)

activate_motors(3)

