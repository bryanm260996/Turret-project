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

# Function to set the speed of a motor
def set_speed(pwm1, pwm2, speed):
    """
    Set the motor speed and direction.
    :param pwm1: PWM object for forward direction.
    :param pwm2: PWM object for reverse direction.
    :param speed: Speed value (-1.0 to 1.0).
    """
    speed = max(min(speed, 1.0), -1.0)  # Clamp speed between -1.0 and 1.0

    if speed > 0:
        pwm1.duty_u16(int(speed * 65500))
        pwm2.duty_u16(0)
    elif speed < 0:
        pwm2.duty_u16(int(-speed * 65500))
        pwm1.duty_u16(0)
    else:
        pwm1.duty_u16(0)
        pwm2.duty_u16(0)

# Movement functions
def pan_right():
    set_speed(pan_servo, pan_servo2, -1)  # Full speed right
    time.sleep(0.1)  # Short action
    set_speed(pan_servo, pan_servo2, 0)   # Stop

def pan_left():
    set_speed(pan_servo, pan_servo2, 1)  # Full speed left
    time.sleep(1)  # Short action
    set_speed(pan_servo, pan_servo2, 0)  # Stop

def tilt_up():
    set_speed(tilt_servo, tilt_servo2, -1)  # Full speed up
    time.sleep(1)  # Short action
    set_speed(tilt_servo, tilt_servo2, 0)  # Stop

def tilt_down():
    set_speed(tilt_servo, tilt_servo2, 1)  # Full speed down
    time.sleep(0.1)  # Short action
    set_speed(tilt_servo, tilt_servo2, 0)  # Stop

# Main loop for input control
print("Control the motors using the following keys:")
print("'a' - Pan left, 'd' - Pan right, 'w' - Tilt up, 's' - Tilt down")
print("Press 'q' to quit.")

try:
    while True:
        command = input("Enter command: ").strip().lower()
        if command == 'a':
            pan_left()
        elif command == 'd':
            pan_right()
        elif command == 'w':
            tilt_up()
        elif command == 's':
            tilt_down()
        elif command == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid command. Use 'a', 'd', 'w', 's', or 'q'.")
except KeyboardInterrupt:
    print("\nProgram interrupted.")

# Clean up resources
pan_servo.deinit()
pan_servo2.deinit()
tilt_servo.deinit()
tilt_servo2.deinit()
print("Resources released. Program terminated.")
