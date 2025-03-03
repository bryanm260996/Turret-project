from machine import PWM, Pin
import time

class MovingTurret:
    def __init__(self, pan_pin_1, pan_pin_2, tilt_pin_1, tilt_pin_2):
        # Define GPIO pins for the pan motor
        self.pan_pin_1 = pan_pin_1
        self.pan_pin_2 = pan_pin_2
        
        # Define GPIO pins for the tilt motor
        self.tilt_pin_1 = tilt_pin_1
        self.tilt_pin_2 = tilt_pin_2

        # Initialize the PWM objects for the pan motor
        self.pan_servo = PWM(Pin(self.pan_pin_1))
        self.pan_servo2 = PWM(Pin(self.pan_pin_2))
        self.pan_servo.freq(50)
        self.pan_servo2.freq(50)

        # Initialize the PWM objects for the tilt motor
        self.tilt_servo = PWM(Pin(self.tilt_pin_1))
        self.tilt_servo2 = PWM(Pin(self.tilt_pin_2))
        self.tilt_servo.freq(50)
        self.tilt_servo2.freq(50)

    def set_speed(self, pwm1, pwm2, speed):
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

    def pan_right(self):
        self.set_speed(self.pan_servo, self.pan_servo2, -1)  # Full speed left
        time.sleep(1)  # Run for 1 second
        self.set_speed(self.pan_servo, self.pan_servo2, 0)   # Stop

    def pan_left(self):
        self.set_speed(self.pan_servo, self.pan_servo2, 1)  # Full speed right
        time.sleep(1)  # Run for 1 second
        self.set_speed(self.pan_servo, self.pan_servo2, 0)  # Stop

    def tilt_down(self):
        self.set_speed(self.tilt_servo, self.tilt_servo2, 1)  # Full speed up
        time.sleep(0.3)  # Run for 1 second
        self.set_speed(self.tilt_servo, self.tilt_servo2, 0)  # Stop

    def tilt_up(self):
        self.set_speed(self.tilt_servo, self.tilt_servo2, -1)  # Full speed down
        time.sleep(0.3)  # Run for 1 second
        self.set_speed(self.tilt_servo, self.tilt_servo2, 0)  # Stop

# Example usage:
if __name__ == "__main__":
    turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)
    
    # Example movements:
    turret.tilt_down()
    turret.pan_right()
    turret.pan_left()
    turret.tilt_up()

