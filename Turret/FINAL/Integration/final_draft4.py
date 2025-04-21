from machine import PWM, Pin, I2C
import time
import ttyacm
import math

# --- Flywheel Controller ---
class FlywheelController:
    INA260_ADDRESS = 0x40
    INA260_CURRENT_REGISTER = 0x01

    def __init__(self, i2c_scl_pin=1, i2c_sda_pin=0, flywheel_pin=15, loader_pin=14):
        self.ina260_i2c = I2C(0, scl=Pin(i2c_scl_pin), sda=Pin(i2c_sda_pin))
        self.flywheel_pin = Pin(flywheel_pin, Pin.OUT)
        self.loader_pin = Pin(loader_pin, Pin.OUT)

    def read_current(self):
        try:
            data = self.ina260_i2c.readfrom_mem(self.INA260_ADDRESS, self.INA260_CURRENT_REGISTER, 2)
            raw_current = int.from_bytes(data, 'big')
            if raw_current & 0x8000:
                raw_current -= 1 << 16
            return raw_current * 1.25
        except OSError:
            print("Error reading INA260.")
            return math.nan

    def desired_shooting(self, num_shots=3, current_threshold=2000, shot_delay=0.4, read_delay=0.03):
        self.flywheel_pin.value(1)
        time.sleep(1)
        self.loader_pin.value(1)
        balls_shot = 0

        while balls_shot < num_shots:
            current = self.read_current()
            time.sleep(read_delay)
            if current > current_threshold:
                self.loader_pin.value(0)
                balls_shot += 1
                time.sleep(shot_delay)
                self.loader_pin.value(1)
                print(f"Shot {balls_shot}")

        self.loader_pin.value(0)
        self.flywheel_pin.value(0)


# --- Moving Turret ---
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
        speed = max(min(speed, 1.0), -1.0)
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

    def stop(self):
        self.move_turret(0, 0)


# --- Turret Controller ---
class TurretController:
    def __init__(self, turret, flywheel=None, port=1, tolerance=8):
        self.tty = ttyacm.open(port)
        self.turret = turret
        self.flywheel = flywheel
        self.tolerance = tolerance
        print(f"Connected to TTY port {port}. Waiting for data...")

    def read_targets(self):
        targets = {}
        while self.tty.any():
            line = self.tty.readline().strip()
            try:
                if line.startswith("Target"):
                    tag, coords = line.split(":")
                    target_num = int(tag.split()[1])
                    x_str, y_str = coords.strip().split(",")
                    x = int(x_str)
                    y = int(y_str)
                    targets[target_num] = (x, y)
            except Exception as e:
                print("Invalid data:", line)
        return targets

    def track_target_for_time(self, target_index, total_duration=6, fire_delay=5):
        kp_x = 0.0111   #0.0102 - #0.0.0109
        kp_y = 0.01107  #0.011 - #0.01106
        kd_x = 0.005
        kd_y = 0.003   #0.005

        desired_x = -18
        desired_y = 50

        last_error_x = 0
        last_error_y = 0

        start_time = time.time()
        fire_triggered = False

        while time.time() - start_time < total_duration:
            targets = self.read_targets()
            if target_index not in targets:
                time.sleep(0.02)
                continue

            x, y = targets[target_index]
            error_x = desired_x - x
            error_y = desired_y - y
            error_x_degrees= error_x*0.043
            error_y_degrees=error_y*0.043


            derivative_x = error_x - last_error_x
            derivative_y = error_y - last_error_y

            pan_speed = max(min(kp_x * error_x + kd_x * derivative_x, 0.4), -0.4)
            tilt_speed = max(min(-kp_y * error_y - kd_y * derivative_y, 0.4), -0.4)

            print(f"Target {target_index} -> Error X: {error_x_degrees}, Y: {error_y_degrees}")

            last_error_x = error_x
            last_error_y = error_y

            if abs(error_x) > self.tolerance or abs(error_y) > self.tolerance:
                self.turret.move_turret(pan_speed, tilt_speed)
                time.sleep(0.03)
                self.turret.stop()
            else:
                print(f"Target {target_index} centered. Holding.")
                if not fire_triggered and (time.time() - start_time >= fire_delay):
                    print(f"🔥 Firing at target {target_index}")
                    if self.flywheel:
                        self.flywheel.desired_shooting()
                    fire_triggered = True

            time.sleep(0.1)

    def run(self):
        overall_start = time.time()

        for i in range(1, 3):  # Targets 1 through 2
            print(f"\nTracking Target {i} for 5 seconds...")
            self.track_target_for_time(i, total_duration=5, fire_delay=4)

        total_elapsed = time.time() - overall_start
        print(f"\n Shot both targets in {total_elapsed:.2f} seconds.")


# --- Main Execution ---
if __name__ == "__main__":
    turret = MovingTurret(pan_pin_1=9, pan_pin_2=10, tilt_pin_1=12, tilt_pin_2=13)
    flywheel = FlywheelController()
    controller = TurretController(turret, flywheel=flywheel, port=1 )
    controller.run()
