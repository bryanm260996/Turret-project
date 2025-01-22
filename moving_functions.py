from machine import PWM, Pin
import time

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

def set_speed(pwm1, pwm2, speed):
    """
    Set the motor speed and direction.
    :param pwm1: PWM object for forward direction.
    :param pwm2: PWM object for reverse direction.
    :param speed: Speed value (-1.0 to 1.0).
    """
    speed = max(min(speed, 1.0), -1.0)  # Clamp speed between -1.0 and 1.0

    if speed > 0:
        pwm1.duty_u16(int(speed * 65535))
        pwm2.duty_u16(0)
    elif speed < 0:
        pwm2.duty_u16(int(-speed * 65535))
        pwm1.duty_u16(0)
    else:
        pwm1.duty_u16(0)
        pwm2.duty_u16(0)

def pan_right():
    set_speed(pan_servo, pan_servo2, -1)  # Full speed left
    time.sleep(1)  # Run for 1 second
    set_speed(pan_servo, pan_servo2, 0)   # Stop
    
def pan_left():
    set_speed(pan_servo, pan_servo2, 1)  # Full speed right
    time.sleep(1)  # Run for 1 second
    set_speed(pan_servo, pan_servo2, 0)  # Stop
    
# Functions for tilt movements
def tilt_down():
    set_speed(tilt_servo, tilt_servo2, 1)  # Full speed up
    time.sleep(1)  # Run for 1 second
    set_speed(tilt_servo, tilt_servo2, 0)  # Stop

def tilt_up():
    set_speed(tilt_servo, tilt_servo2, -1)  # Full speed down
    time.sleep(1)  # Run for 1 second
    set_speed(tilt_servo, tilt_servo2, 0)  # Stop


    
tilt_down()