import machine
import time

# Define GPIO pins for the pan and tilt motors
PAN_PIN = 9  
TILT_PIN = 12  

# Set the PWM frequency (50Hz is common for servos)
PWM_FREQUENCY = 50

# Create PWM objects for pan and tilt
pan_pwm = machine.PWM(machine.Pin(PAN_PIN))
tilt_pwm = machine.PWM(machine.Pin(TILT_PIN))

# Set the frequency for both PWM channels
pan_pwm.freq(PWM_FREQUENCY)
tilt_pwm.freq(PWM_FREQUENCY)


# Function to set the angle for a motor
def set_angle(pwm, angle):
    """
    Set the motor to a specific angle.
    :param pwm: The PWM object controlling the motor.
    :param angle: Desired angle (0 to 180 degrees).
    """
    # Convert the angle to a duty cycle value (500 to 2500 µs pulse width)
    duty_cycle = int((angle / 180) * (2000) + 500)
    # Set the duty cycle in nanoseconds
    pwm.duty_ns(duty_cycle * 1000)


try:
    while True:
        # Sweep from 0 to 180 degrees
        for angle in range(0, 181, 5):
            set_angle(pan_pwm, angle)
            time.sleep(0.05)
        
        # Sweep from 180 to 0 degrees
        for angle in range(180, -1, -5):
            set_angle(pan_pwm, angle)
            time.sleep(0.05)

except KeyboardInterrupt:
    # Stop the PWM signal if the program is interrupted
    pan_pwm.deinit()